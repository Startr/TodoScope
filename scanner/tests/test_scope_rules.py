"""Scope rules: .todoscope-exclude.csv with an optional mode column.

exclude (the default) keeps a path out of the scan. hide scans it but marks
its cards so the board can fold them away. The board's scope editor writes
the file back through /api/scope, local repos only, guarded by a file hash.

Tests monkeypatch the repo registry and auth instead of writing them, so a
run never touches the real local_repos.yaml or access_keys.csv.
"""
import json
import subprocess

import pytest

import scanner.app as appmod
from scanner import fragments


def _repo(tmp_path, scope_csv=None):
    fix = tmp_path / 'scoperepo'
    (fix / 'charts' / 'demo').mkdir(parents=True)
    (fix / 'build').mkdir()
    subprocess.run(['git', 'init', '-q', str(fix)], check=True)
    (fix / 'a.py').write_text('# TODO: keep me\n')
    (fix / 'charts' / 'demo' / 'b.py').write_text('# TODO: chart work\n')
    (fix / 'charts' / 'demo' / 'TODO.md').write_text('## TODO\n\n- [ ] **Chart card**: plan\n')
    (fix / 'build' / 'c.py').write_text('# TODO: generated\n')
    if scope_csv is not None:
        (fix / '.todoscope-exclude.csv').write_text(scope_csv)
    return fix


@pytest.fixture
def client(tmp_path, monkeypatch):
    fix = _repo(tmp_path, 'path,reason,mode\nbuild,generated,\ncharts,plans,hide\n*.min.js,minified,\n')
    (fix / 'x.min.js').write_text('// TODO: minified\n')
    monkeypatch.setattr(appmod, 'load_access_keys', lambda: set())
    monkeypatch.setattr(appmod, 'load_local_repos',
                        lambda: {'scoperepo': {'path': str(fix), 'public': False}})
    appmod.app.config['TESTING'] = True
    return appmod.app.test_client(), fix


def test_mode_column_parses_and_defaults_to_exclude(tmp_path):
    fix = _repo(tmp_path, 'path,reason,mode\nbuild,generated,\ncharts,plans,HIDE\nvendor,x,bogus\n')
    rules = appmod.load_scope_rules(str(fix))
    assert [(r['path'], r['mode']) for r in rules] == [
        ('build', 'exclude'), ('charts', 'hide'), ('vendor', 'exclude')]
    exclusions, hidden = appmod.split_scope(rules)
    assert [r['path'] for r in exclusions] == ['build', 'vendor']
    assert [r['path'] for r in hidden] == ['charts']


def test_two_column_file_still_means_exclude(tmp_path):
    fix = _repo(tmp_path, 'path,reason\nbuild,generated\n')
    assert appmod.load_exclusions(str(fix)) == [
        {'path': 'build', 'reason': 'generated', 'mode': 'exclude'}]


def test_hidden_paths_are_still_scanned(tmp_path):
    fix = _repo(tmp_path, 'path,reason,mode\nbuild,generated,\ncharts,plans,hide\n')
    files = {t.file_path for t in appmod.find_todos(str(fix), exclusions=appmod.load_exclusions(str(fix)))}
    assert 'charts/demo/b.py' in files
    assert 'build/c.py' not in files


def test_hide_rules_do_not_change_the_cache_hash(tmp_path):
    a = _repo(tmp_path, 'path,reason\nbuild,generated\n')
    before = appmod.exclusions_hash(appmod.load_exclusions(str(a)))
    (a / '.todoscope-exclude.csv').write_text('path,reason,mode\nbuild,generated,\ncharts,plans,hide\n')
    assert appmod.exclusions_hash(appmod.load_exclusions(str(a))) == before


def test_fragments_mark_hidden_cards_without_dropping_them():
    hidden = [{'path': 'charts', 'reason': 'plans', 'mode': 'hide'}]
    with appmod.app.app_context():
        html = fragments.render_todos_list_html([
            {'file_path': 'a.py', 'line_num': 1, 'todo_text': '# TODO: a', 'next_line': None},
            {'file_path': 'charts/x.py', 'line_num': 1, 'todo_text': '# TODO: b', 'next_line': None},
        ], hidden=hidden)
    assert html.count('class="todo-item td-hidden"') == 1
    assert html.count('class="todo-item"') == 1


def _events(resp):
    return [json.loads(l[len('data: '):]) for l in resp.get_data(as_text=True).splitlines()
            if l.startswith('data: ')]


def test_stream_sends_scope_and_marks_hidden_board_cards(client):
    c, _fix = client
    events = _events(c.get('/stream_data/scoperepo?refresh=1'))
    scope = next(e for e in events if e['type'] == 'scope')
    assert {r['path']: r['mode'] for r in scope['rules']} == {
        'build': 'exclude', 'charts': 'hide', '*.min.js': 'exclude'}
    assert scope['hash']
    board = [e for e in events if e['type'] == 'kanban'][-1]['html']
    assert 'td-hidden' in board and 'Hidden by charts' in board
    # Directory rules prune the walk; only file-level matches are listed
    excluded = next(e for e in events if e['type'] == 'excluded')
    assert [i['path'] for i in excluded['items']] == ['x.min.js']


def test_scope_post_writes_file_and_drops_mode_column_when_unused(client):
    c, fix = client
    base = appmod.scope_file_hash(str(fix))
    resp = c.post('/api/scope/scoperepo', json={'base_hash': base, 'rules': [
        {'path': './build/', 'reason': 'generated\noutput', 'mode': 'exclude'}]})
    assert resp.status_code == 200, resp.get_json()
    assert (fix / '.todoscope-exclude.csv').read_text() == 'path,reason\nbuild,generated output\n'
    assert resp.get_json()['hash'] == appmod.scope_file_hash(str(fix))


def test_scope_post_quotes_reasons_with_commas(client):
    c, fix = client
    base = appmod.scope_file_hash(str(fix))
    resp = c.post('/api/scope/scoperepo', json={'base_hash': base, 'rules': [
        {'path': 'charts', 'reason': 'plans, parked', 'mode': 'hide'}]})
    assert resp.status_code == 200
    assert appmod.load_scope_rules(str(fix)) == [
        {'path': 'charts', 'reason': 'plans, parked', 'mode': 'hide'}]


def test_scope_post_refuses_stale_hash(client):
    c, fix = client
    original = (fix / '.todoscope-exclude.csv').read_text()
    resp = c.post('/api/scope/scoperepo', json={'base_hash': 'stale', 'rules': []})
    assert resp.status_code == 409
    assert len(resp.get_json()['rules']) == 3
    assert (fix / '.todoscope-exclude.csv').read_text() == original


@pytest.mark.parametrize('bad', [
    {'path': '../outside', 'mode': 'exclude'},
    {'path': '/etc', 'mode': 'exclude'},
    {'path': 'docs', 'mode': 'shrug'},
    {'path': '   ', 'mode': 'hide'},
])
def test_scope_post_rejects_bad_rules(client, bad):
    c, fix = client
    resp = c.post('/api/scope/scoperepo', json={
        'base_hash': appmod.scope_file_hash(str(fix)), 'rules': [bad]})
    assert resp.status_code == 400


def test_scope_post_rejects_duplicates(client):
    c, fix = client
    resp = c.post('/api/scope/scoperepo', json={
        'base_hash': appmod.scope_file_hash(str(fix)),
        'rules': [{'path': 'docs', 'mode': 'hide'}, {'path': 'docs/', 'mode': 'exclude'}]})
    assert resp.status_code == 400


def test_scope_post_is_local_repos_only(client):
    c, _fix = client
    resp = c.post('/api/scope/someclone', json={'base_hash': '', 'rules': []})
    assert resp.status_code == 403
