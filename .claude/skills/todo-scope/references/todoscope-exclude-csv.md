# TodoScope: `.todoscope-exclude.csv`

## `.todoscope-exclude.csv`

CSV format with `path,reason` columns and an optional `mode` column:

```csv
path,reason,mode
node_modules,dependency cache,
build,generated files,
dist,generated files,
__pycache__,Python bytecode cache,
.venv,virtual environment,
vendor,third-party dependencies,
charts,navigation plans — useful but not every day,hide
```

- **`exclude`** (blank or missing `mode`): the path is never scanned.
- **`hide`**: the path is scanned, but its cards fold away behind the
  board's *Show hidden* toggle. Use it for work that is real but not
  always in focus, such as `charts/` navigation plans.

A path matches its whole subtree; globs such as `*.min.js` work too. A
two-column file stays valid. On local repos the board's *Scan scope* panel
edits this file directly.
