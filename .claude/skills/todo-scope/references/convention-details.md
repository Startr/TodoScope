# TodoScope: convention details

### Organizational Extras (Nice-to-Have, Not Card-Generating)

These improve readability in the markdown file but do not affect card
generation:

**Subsection headers** (`###`) group related cards visually within a
column. The scanner does not map these to columns. Use them for topic
areas, version milestones, or categories:
`### v2.x — Near Term`, `### From Codebase (untracked)`,
`### [CSS] Framework Improvements`.

**Prose and context** (paragraphs, blockquotes, explanatory text between
items) is shown in the TodoScope interface but does not become a card.
Leave it in place — it's documentation, not a work item.

**Attribution** for items surfaced by reviews or external input:
`*(Surfaced by Name in context, YYYY-MM-DD.)*`

**Inline cross-references** link a TODO.md item to its source location:
`<!-- inline: file.py:123 -->` on the line below the subtask. Multiple
locations separated by spaces: `<!-- inline: audio.py:598,652 ollama.py:1699 -->`.

**"From Codebase (untracked)"** is a subsection under `## TODO` for
inline tags found by the scanner that don't yet have a corresponding
TODO.md entry. Group them by area (Backend, Frontend, etc.) with a
parent card summarizing the batch and subtasks listing individual
locations.

### Kanban Column Mapping

It's important to get the column mapping right. Backlog items are often less urgent, TODO is the main queue, In Progress signals active work, Bugs need special attention, and Done tracks completed work. The scanner relies on this structure to place cards correctly. If the mapping is off, the board won't reflect reality.
