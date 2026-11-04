---
name: todo-scope
description: Bootstrap and align a repo's TODO.md to TodoScope conventions. Creates TODO.md if missing, restructures messy ones, sets up .todoscope-exclude.csv, and adds cleanup TODOs for remaining work. Use when setting up a TODO.md, restructuring a roadmap, aligning a repo with TodoScope conventions, or running "todo-scope" on a project.
argument-hint: (no arguments)
---

# TodoScope — TODO.md Bootstrap & Alignment

Bootstrap and align a repo's `TODO.md` to
[TodoScope](https://github.com/Startr/TodoScope) conventions. This is housekeeping, not deep scanning. The TodoScope app handles scanning. This gets a repo's `TODO.md` into shape so the scanner can read it.

## Prerequisite

The TodoScope app must be installed: `brew install --cask sage-is/apps/todoscope`, or clone and build [Startr/TodoScope](https://github.com/Startr/TodoScope).

Canonical copy: `Startr/TodoScope/.claude/skills/todo-scope`; keep the two in sync.

## What This Does

One behavior, no modes. When invoked:

1. **Check for `.todoscope-exclude.csv`** — if missing, ask the user what paths to exclude and create it.
2. **Read the existing `TODO.md`** — if it exists, assess how far it has drifted from the convention. If it doesn't exist, create one.
3. **Restructure `TODO.md`** to conform — preserve existing content, reshape sections, ensure every actionable item has a checkbox, fix nesting.
4. **Add TODO items for remaining cleanup** — inline tag migration, exclude path review, whatever the repo still needs to be fully TodoScope-compatible.
5. **Offer to help** with those cleanup tasks.
6. **Encourage a convention sync check.** After everything is done, suggest the user scan the repo with their TodoScope instance and verify the board looks right. If columns or mappings don't match what they expect, offer to update this file to match.

## The Convention

The authoritative convention lives in TodoScope's `kanban.py`. We must mirror it, not the other way around — the scanner is the source of truth. The convention is:

### Inline Tags → Columns

Three tags. That's it.

| Inline tag | Kanban column  |
|------------|----------------|
| `TODO:`    | TODO           |
| `FIXME:`   | In Progress    |
| `BUG:`     | Bugs           |

`NOTE:` is informational — documentation, not a work item. Not tracked.
`DEPRECATED:` tags should be tracked as TODO items for removal at the
stated version.

Backlog has no inline tag — items land there by being placed under a
`## Backlog` section header, not by annotation.

### Section Headers → Columns

`TODO.md` section headers map to columns via case-insensitive substring
matching. Multiple aliases are supported:

| Column      | Accepted headers                                |
|-------------|-------------------------------------------------|
| In Progress | `In Progress`, `Doing`, `WIP`, `High Priority`  |
| TODO        | `TODO`, `Medium Priority`, `Tech Debt`           |
| Backlog     | `Backlog`, `Low Priority`                        |
| Bugs        | `Bugs`, `Bug`                                    |
| Done        | `Done`, `Completed`                              |

Projects can use whichever alias fits their context. `High Priority` and
`In Progress` are interchangeable. The scanner handles the mapping.

### Hashtags

Two functional tags affect board behavior:

- `#critical` — elevates a card to the top of its column
- `#bug` — overrides column placement to Bugs

All other hashtags (`#brand`, `#api`, `#ux`, etc.) are metadata — displayed
on the kanban card as inline code badges but not acted on. Tags are never
stripped; they travel with the card from TODO.md to the board. Use them
freely to describe the kind of work.

### Card Generation — The Ontology That Matters

This is the structure that produces kanban cards. Everything else is
cosmetic. Get this right and the board works.

```
## Section Header              ← determines the kanban COLUMN
- [ ] **Card Title**: Desc     ← becomes a CARD on the board
  - [ ] Subtask one            ← becomes a CHECKLIST ITEM on the card
  - [x] Subtask done           ← checked item on the checklist
```

One `## header` → one column. One `- [ ] parent` → one card. Indented
`- [ ] children` → the checklist rendered on that card. That's the full
ontology.

A worked example, two full reference TODO.md files and what to notice in them: [references/examples.md](references/examples.md).

**Parent items** (the cards) need:
- A checkbox: `- [ ]` or `- [x]`
- A clear title, optionally bold: `- [ ] **Title**: Description`
- Optional category tag in brackets: `[EXTERNAL]`, `[SITE]`, `[MIXED]`
- Optional stakeholder: `(Stakeholder: Name)` or `(Name)`
- Optional hashtags: `#critical`, `#api`, `#ux`

**Subtasks** (the checklist) are indented under their parent with their
own checkboxes. Completion status is glanceable on the board without
opening the file. Keep nesting shallow — two levels is typical, three
is the practical maximum.

**Checked items** (`- [x]`) always land in the Done column, regardless
of which section they sit in. Normalize `[X]` to lowercase `[x]`.

**No stray cards.** A run of single-line parent items with no checklists
is a smell — each one becomes a bare card and the board turns into a flat
list. Group related one-liners under a thematic parent card and demote
them to subtasks:

```markdown
<!-- Strays — each becomes a bare card -->
- [ ] **Add search/filter to the Repositories table** #ux
- [ ] **Add a "last scanned" timestamp** per repo row #ux

<!-- Grouped — one card with a glanceable checklist -->
- [ ] **Repositories table tooling**: search, freshness #ux
  - [ ] Add search/filter to the Repositories table
  - [ ] Add a "last scanned" timestamp per repo row
```

A standalone parent is fine when it is a genuinely independent effort
with a rich description. Three or more sibling one-liners on the same
theme always get a parent.

### Organizational Extras (Nice-to-Have, Not Card-Generating)

Subsection headers, prose, attribution, inline cross-references, "From Codebase (untracked)", and the column-mapping note: [references/convention-details.md](references/convention-details.md).

### Multiple TODO.md Files

The scanner finds TODO.md files in subdirectories too. Each card tracks
which file it came from (`TODO.md`, `docs/TODO.md`, etc.) and its line
number. When restructuring, respect the existing file locations — don't
consolidate subdirectory TODO.md files into the root unless asked.

## `.todoscope-exclude.csv`

Format, the `mode` column and path matching: [references/todoscope-exclude-csv.md](references/todoscope-exclude-csv.md).

If the file doesn't exist, ask the user what to exclude. Common candidates:
dependency caches, build output, virtual environments, vendored code.
Ask separately whether any live-but-noisy paths should be `hide` instead.

## Convention Header

Every TODO.md that follows the convention should include this header block
(or similar) so contributors understand the column mapping at a glance:

The block: [references/convention-header.md](references/convention-header.md).

## Rules for Restructuring

- **Preserve existing content.** Don't delete items. Reshape sections, fix
  formatting, add missing checkboxes. Move checked items to Done/Completed.
- **Preserve existing grouping.** If the TODO.md uses version milestones,
  topic areas, or subsection headers, keep them.
- **Fix nesting.** Items that are subtasks of a larger effort should be nested
  under the parent, not listed as independent top-level items.
- **Group strays.** Runs of single-line parents with no checklists get
  grouped under thematic parent cards (see "No stray cards" above). When
  assessing an existing TODO.md, count strays and flag them — this is the
  most common drift.
- **Add checkboxes.** Every actionable item needs `- [ ]` or `- [x]`.
  Markdown list items and todo items become kanban cards. Other content
  (prose, headers, blockquotes) is shown in the TodoScope interface but
  doesn't land on the board.
- **Clean up empties.** Remove blank checkboxes, trailing whitespace, orphaned
  list markers.
- **Don't duplicate.** If an item already exists, don't add it again.
- **Add cleanup TODOs.** After restructuring, add items for remaining work
  the repo needs to be fully TodoScope-compatible:
  - Migrate inline tags to `TODO:` / `FIXME:` / `BUG:` conventions
  - Review `.todoscope-exclude.csv` paths
  - Any other alignment work discovered during assessment
- **Keep it concise.** Short sentences. No empty modifiers.

## What This Does NOT Do

- **No scanning.** Do not search source files for inline tags.
  TodoScope the application does that.
- **No regex.** Do not perform comment-syntax pattern matching.
- **No cross-referencing.** Do not perform fuzzy matching between inline tags and TODO.md
  items.
- **No KANBAN.canvas editing.** That file auto-generates from TodoScope. Never
  hand-edit it.
- **No `.todoscope-snapshot.json` or `.todoscope-done.json` editing.** These
  are scanner-managed files for tracking inline TODO completion over time.
