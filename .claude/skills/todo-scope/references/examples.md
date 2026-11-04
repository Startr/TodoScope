# TodoScope: reference examples

The larger example's "convention header as above" is [convention-header.md](convention-header.md).

## Reference Examples

Two anonymized examples based on real projects. Study the hierarchy — section
headers set the column, subsection headers group, parent items become cards,
subtasks nest under them.

### Small project (nonprofit site)

```markdown
# TODO - Project Development Tasks

## High Priority

- **Questions for Board/Stakeholders:**
  - [ ] Verify fundraising goal amount
  - [ ] Request photos/bios for team profiles
  - [ ] Get confirmed list of volunteers
- [ ] [EXTERNAL] Business Registration Verification (Stakeholder: J.D.) #critical
  - [ ] Add English trade name in provincial registry
  - [ ] Initiate registration with provincial authority
  - [ ] Update donation platform and social media profiles
- [ ] Annual Fundraising Event — Thank-You Presentation
  - [ ] [EXTERNAL] Content & Media To Confirm (Stakeholder: V.K. / J.D.)
  - [ ] Obtain video testimony — confirm availability, length, quality
  - [ ] Collect confirmed impact numbers from recent program
- [ ] [MIXED] Event Logistics & Materials (Stakeholder: V.K.)
  - [ ] Prepare sponsorship one-pagers or table cards
  - [ ] Test A/V setup for preview playback

## Medium Priority

- [ ] [EXTERNAL] Donation Portal Configuration (Stakeholder: J.D.)
  - [ ] Upload logo files (PNG, SVG, JPG formats)
  - [ ] Create donation designations
  - [x] Test donation flow (small test transaction)
  - [ ] Configure recurring donation option

- [ ] [SITE] Translation Corrections (M.L.)
  - [ ] Audit all translated pages
  - [ ] Correct organization name across languages
  - [ ] Review key term translations

## Backlog

### [CSS] Framework Improvements
- [ ] **Host CSS Locally**: Eliminate external dependency
  - [ ] Download and save CSS as local file
  - [ ] Update templates to link local file
  - [ ] Test site functionality and commit

## Completed

- [x] [SITE] Legal Footer Implementation (M.L.)
    - [x] Verify registration number with public registry
    - [x] Add footer to all pages
    - [x] Test visibility and commit
```

### Larger project (application with backend and frontend)

```markdown
# Roadmap

This file tracks active work only.

> **Convention** — Sections map to kanban columns...
> (convention header as above)

## In Progress

- [ ] **Docker Image Slimming**: Reduce image size (Team Lead)
  - [x] Hit the ~2.5GB target (down from 9.7GB)
  - [ ] Hit the ~1.5GB base-image target after trimming heavy deps

## TODO

### v2.x — Near Term

- [ ] **Auth & Onboarding**: Email notifications and LDAP consolidation
  - [ ] Outgoing email notifications (reuse bridge SMTP config)
  - [ ] Consolidate LDAP config into Auth/Integrations tab

- [ ] **Frontend Toolchain Upgrade**: Framework and bundler updates
  - [ ] Framework v4 → v5
  - [ ] Bundler v5 → v6
  - [ ] Meta-framework to latest

- [ ] **Codebase Cleanup**: Namespace renames, semantic HTML, branding
  - [ ] DB migration (Alembic rename of tables, columns, enum values)
  - [ ] Rename `components/legacy/` directory → `components/current/`
  - [ ] Scrub remaining upstream references in comments and defaults

### v3.0 — Future

- [ ] **Backend Rewrite Research**: Evaluate framework options
  - [ ] Review research doc with team
  - [ ] Generate contract test suite from OpenAPI spec
  - [ ] Phase 0 spike: chosen framework + streaming proxy

### From Codebase (untracked)

- [ ] **Backend Inline TODOs**: Load balancing, type updates, deprecation removal
  - [ ] Intelligent load balancing for multiple backends (`api.py:1`)
  - [ ] Add retries to audio processing requests (`audio.py:1120`)
  - [ ] Remove deprecated env var fallback at next major version (`env.py:393`)

- [ ] **Frontend Inline TODOs**: UX polish, component upgrades
  - [ ] Filter order handling in model config (`Selector.svelte:34`)
  - [ ] Emoji picker search filtering (`EmojiPicker.svelte:47`)
  - [ ] Update rich text editor components to v3 (`Editor.svelte:79`)

## Backlog

- [ ] **CI/CD Pipeline**: Gated releases, scanning, regression tests
  - [ ] `make scan_container` — image scanning (post-build)
  - [ ] `make lint` — linter rollup
  - [ ] Staging instance for pre-prod testing
    <!-- inline: Makefile:572 -->
  - [ ] Browser regression tests
  - [ ] DAST scanning via `make scan_dast`

## Bugs

_No known bugs. Use `# BUG:` inline tags to flag defects in source._

## Done

> Completed items are moved to `docs/completed-todos.md` periodically.

- [x] TodoScope Alignment
  - [x] Restructure TODO.md to conventions
  - [x] Fix duplicate rows in `.todoscope-exclude.csv`
  - [x] Run scanner and verify kanban board matches expectations
```

### What to notice

- **Convention header** at the top explains the column mapping for contributors.
- **Section headers** set the column. Both files use aliases (`High Priority`,
  `Completed`, `In Progress`) that the scanner maps automatically.
- **Subsection headers** (`###`) group without affecting column placement.
  Version milestones (`### v2.x`), topic areas (`### From Codebase`).
- **Parent items** are the cards. Each has a checkbox and a clear title.
- **Subtasks** nest under parents. Two levels is typical.
- **Inline cross-references** (`<!-- inline: file:line -->`) link items
  to source locations.
- **"From Codebase (untracked)"** groups inline TODOs found by the scanner
  that haven't been manually curated yet.
- **Prose blocks** stay in place — visible in the interface, not cards.
- **Category tags** (`[EXTERNAL]`, `[SITE]`) and **stakeholder assignments**
  live on the parent line.
- **Completed items** use `- [x]` and sit in a `Done`/`Completed` section.
- **Archive reference** points to where completed items get bulk-moved.

### Card Generation — The Ontology That Matters

Example — this markdown:

```markdown
## In Progress

- [ ] **Docker Image Slimming**: (Team Lead)
  - [x] Hit the ~2.5GB target (down from 9.7GB)
  - [ ] Hit the ~1.5GB base-image target after trimming heavy deps
```

generates one column ("In Progress") with one card ("Docker Image
Slimming") showing a two-item checklist, one checked. 
