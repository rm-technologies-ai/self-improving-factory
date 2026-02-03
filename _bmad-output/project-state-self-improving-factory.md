# Project State: self-improving-factory

---
bmad_type: project-state
bmad_version: 6.0.0-Beta.5
project_name: self-improving-factory
project_path: ~/repos/self-improving-factory
status: initialized
session_date: 2026-02-03
---

## BMAD Workflow Status

```yaml
current_phase: requirements-capture
current_step: operational-mode-established
next_step: receive-implementation-patterns
blockers: []
operational_mode: continuous-requirements-capture
```

---

## Operational Mode: Continuous Requirements Capture

**ACTIVE:** All sessions operate in this mode until project completion.

### Mode Rules

1. **Immediate Documentation** - Requirements from prompts documented instantly as PRD entries
2. **TDD-First** - Each requirement includes test criteria before implementation
3. **Traceability** - All requirements get unique IDs (REQ-XXX, NFR-XXX)
4. **State Persistence** - State saved immediately after every significant change
5. **Session Recovery** - All artifacts support restoration from failure state

### Workflow Per Requirement

```
User provides requirement → Document in PRD → Define acceptance criteria → Define TDD test criteria → Persist state → Acknowledge
```

---

## Project Brief

### Purpose

Greenfield project for **headless/autonomous project provisioning**. The system provisions new projects or repos with:

- Initialization
- Maintenance updates
- Feature additions/removals
- Idempotent and graceful operations
- Compensation logic and exception handling
- Autonomous error recovery

### Core Requirements

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **Idempotent Operations** | All operations must be repeatable without side effects | CRITICAL |
| **Compensation Logic** | Proper rollback and recovery from errors | CRITICAL |
| **Exception Handling** | Autonomous error recovery and continuation | CRITICAL |
| **Headless Operation** | No human-in-the-loop for standard operations | HIGH |
| **Data-Driven Components** | User-defined component templates by project type | HIGH |
| **State Persistence** | Immediate state save for session/failure recovery | HIGH |

### Initial Provisioning Steps

1. Creation of local repository
2. Initialization and support files
3. Integration with Git
4. Installation of data-driven components

---

## Test Environment

### Test Project

| Property | Value |
|----------|-------|
| Location | `~/repos/test-project` |
| Git Status | Initialized, pushed to GitHub |
| Purpose | Development and E2E testing |

### Teardown Protocol

- Delete everything locally **except** the project folder
- Preserves folder structure for rapid dev/test cycles
- Enables frequent E2E and regression testing

### Feature Flags

| Flag | Purpose | Default |
|------|---------|---------|
| `ENABLE_REMOTE_PROVISIONING_TESTS` | Control GitHub remote operations during testing | `false` |

**Rationale:** Prevents issues during sequential unit tests and frequent E2E testing. Tests flagged for remote operations are skipped until flag is enabled and expected results are updated.

---

## Requirements Management

### Input Sources

1. **User Prompts** - Incremental requirements via conversation
2. **docs/ Folder** - Text files with specifications

### Output Persistence

All new features and requirements are immediately stored in:
- `_bmad-output/` folder
- Preserves current development state
- Enables session recovery
- Supports failure state restoration

---

## Legacy Project Reference

### Source Project

| Property | Value |
|----------|-------|
| Name | project-setup |
| Path | `~/repos/project-setup` |
| Status | Legacy (extraction source) |
| Catalog | `discovery-catalog-project-setup-legacy.md` |

### Extraction Strategy

Controlled distillation of specifications and code from legacy project into new architectural framework.

---

## Working Repositories

| Repository | Path | Purpose |
|------------|------|---------|
| **self-improving-factory** | `~/repos/self-improving-factory` | Main development (this project) |
| **project-setup** | `~/repos/project-setup` | Legacy extraction source |
| **test-project** | `~/repos/test-project` | E2E testing target |
| **rm-claude-code** | `~/repos/rm-claude-code` | CLAUDE.md variants reuse library |

---

## Completed Activities

### 2026-02-03

- [x] Project initialization acknowledged
- [x] BMAD config loaded (user: Roy, lang: English)
- [x] Legacy project discovery completed
- [x] Discovery catalog created: `discovery-catalog-project-setup-legacy.md`
- [x] Project state persisted: `project-state-self-improving-factory.md`
- [x] Continuous Requirements Capture Mode established
- [x] Incremental PRD created: `prd-self-improving-factory-incremental.md`
- [x] CLAUDE.md created with operational memories
- [x] Initial requirements (REQ-001 to REQ-013, NFR-001 to NFR-004) documented
- [x] Software Reuse Library Management requirements added (REQ-014, REQ-015)
- [x] Planned libraries registered: rm-python, rm-typescript, rm-skills (definitions pending)
- [x] Project-Scope Installation Principle added (REQ-016) - FOUNDATIONAL
- [x] SQLite Optional Component added (REQ-017)
- [x] SQLite IMPLEMENTED at project scope (.data/factory.db)
- [x] Migration system created (db/migrate.py)
- [x] Initial schema with 10 tables created
- [x] Seeded 17 requirements, 4 NFRs, 3 reuse libraries, project state
- [x] REQ-018: rm-claude-code Reuse Library defined (CLAUDE.md variants + DAG catalogs)
- [x] rm-claude-code library registered in database
- [x] REQ-019: BMAD Method Installation Component defined (mandatory default, headless)
- [x] bmad-method component registered in database
- [x] REQ-020: Production Enterprise Grade variant defined (first rm-claude-code variant)
- [x] production-enterprise-grade template registered in database
- [x] REQ-021: Library-First Asset Management Pattern defined (CRITICAL operational pattern)
- [x] REQ-022: Prompt Segments Database IMPLEMENTED (4 tables, 7 indexes)
- [x] production-enterprise-grade composition initialized in database
- [x] Requirement scope clarified: all requirements apply to factory AND descendants
- [x] Prompt segment: peg-feedback-loop-rules (sequence: 10)
- [x] Prompt segment: peg-solid-principles (sequence: 20, front-matter)
- [x] Prompt segment: peg-operating-disposition (sequence: 30, L4 autonomous)
- [x] Prompt segment: peg-tdd-principles (sequence: 40, Red-Green-Refactor)
- [x] Prompt segment: peg-dry-principles (sequence: 50, library-first reuse)
- [x] Prompt segment: peg-data-driven-principles (sequence: 60, no hardcode)
- [x] Prompt segment: peg-resiliency-principles (sequence: 70, compensation/recovery)
- [x] Prompt segment: peg-security-principles (sequence: 80, OWASP/secrets)
- [x] Prompt segment: peg-claude-add-reference (sequence: 90, project extensions)
- [x] Template: tpl-claude-add-md (CLAUDE-ADD.md template for rm-claude-code)
- [x] Prompt segment: peg-source-control-skills (sequence: 100, skill reference)
- [x] Skill extracted: skill-create-issue (idempotent GitHub issue creation)
- [x] Skill created: skill-start-work (branch creation, checkout)
- [x] Skill created: skill-complete-work (autonomous PR, unattended merge)
- [x] Prompt segment: peg-repo-structure (sequence: 110, stack de facto conventions)
- [x] Library asset: lib-claude-md-peg (composed CLAUDE.md for production-enterprise-grade variant)
- [x] REQ-023: CLAUDE.md Deployment to Descendant Projects defined
- [x] rm-claude-code repository created at ~/repos/rm-claude-code
- [x] production-enterprise-grade variant deployed with CLAUDE.md, DAG.md, 3 skills
- [x] CI workflow created for variant validation
- [x] Refactored save-context → save-state (BMAD integration)
- [x] Refactored load-context → load-state (BMAD integration)
- [x] Skills added to rm-claude-code library
- [x] Deprecated .claude/context/ in favor of _bmad-output/ state management
- [x] Test infrastructure created (tests/unit/, tests/integration/)
- [x] Integration test: Quickflow agent Python hello world smoke test
- [x] pytest configured with markers (integration, slow, requires_claude)
- [x] Structure tests verify provisioning (5 tests passing)
- [x] REQ-019 updated: BMAD uses upstream installer (npx bmad-method install)
- [x] REQ-024 added: Headless BMAD Installation Wrapper (for autonomous provisioning)
- [x] Test fixtures updated with BMAD installer mode (pending REQ-024)

---

## Next Actions

1. **Architecture Design** - Define new architectural framework for headless provisioning
2. **Specification Extraction** - Begin controlled extraction from legacy project
3. **Component Template System** - Design data-driven component templates
4. **Compensation Framework** - Design error handling and rollback patterns
5. **Test Infrastructure** - Set up test framework with feature flags

---

## Session Recovery Information

```yaml
last_agent: quick-flow-solo-dev (Barry)
last_activity: req-023-claude-md-deployment
last_artifact: prd-self-improving-factory-incremental.md
recovery_point: continuous-requirements-capture-active
operational_mode: continuous-requirements-capture
context_files:
  - _bmad-output/discovery-catalog-project-setup-legacy.md
  - _bmad-output/project-state-self-improving-factory.md
  - _bmad-output/prd-self-improving-factory-incremental.md
  - CLAUDE.md
```

---

## Document Footer

```yaml
created_by: Barry (Quick Flow Solo Dev)
created_at: 2026-02-03
last_updated: 2026-02-03
version: 1.2.0
status: active
change_log:
  - "1.0.0: Initial project state"
  - "1.1.0: Added Continuous Requirements Capture Mode"
  - "1.2.0: Added REQ-023 (CLAUDE.md Deployment) and lib-claude-md-peg library asset"
```
