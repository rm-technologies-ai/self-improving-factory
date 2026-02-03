# CLAUDE.md - Self-Improving Factory

## Project Overview

**Self-Improving Factory** is a headless/autonomous project provisioning system.

## Operational Mode: Continuous Requirements Capture

**CRITICAL:** This project operates in **Continuous Requirements Capture Mode**:

1. **Immediate Documentation** - All requirements provided via prompts are documented immediately as PRD entries
2. **TDD-First** - Each requirement includes TDD test criteria before implementation
3. **Traceability** - All requirements get unique IDs (REQ-XXX, NFR-XXX)
4. **State Persistence** - State saved immediately to `_bmad-output/` after every significant change
5. **Session Recovery** - All artifacts support session restoration from failure state

### Requirements Capture Process

```
User provides requirement
    ↓
Document in PRD with unique ID
    ↓
Define acceptance criteria
    ↓
Define TDD test criteria
    ↓
Persist state immediately
    ↓
Acknowledge to user
```

### Key Files

| File | Purpose |
|------|---------|
| `_bmad-output/prd-self-improving-factory-incremental.md` | Living PRD with all requirements |
| `_bmad-output/project-state-self-improving-factory.md` | Current project state and workflow status |
| `_bmad-output/discovery-catalog-project-setup-legacy.md` | Legacy project extraction reference |

## Engineering Principles

### Project-Scope Installation (FOUNDATIONAL)
**All components must install at project scope level for portability and self-containment.**
- Components are self-contained within the repository
- Repository is portable (clone and run without global dependencies)
- Non-project-scope components cataloged in dependency manifest
- Idempotent provisioning handles external dependencies gracefully

### Idempotent Operations
All operations must be repeatable without side effects.

### Compensation Logic
All operations must have rollback procedures for error recovery.

### Exception Handling
- Catch and categorize all exceptions
- Retry transient errors with backoff
- Trigger compensation for non-recoverable errors
- Continue processing independent operations

### Data-Driven Design
- Component templates defined in configuration
- Project types drive component selection
- Variable substitution for customization

## Database Infrastructure

**SQLite is installed at project scope** (REQ-017 IMPLEMENTED)

### Database Location
- **Path:** `.data/factory.db`
- **Migrations:** `db/migrations/*.py`
- **Migration Runner:** `python db/migrate.py [up|down|status|reset]`
- **Python API:** `from db import get_requirement, add_requirement, ...`

### Schema (14 Tables)
| Table | Purpose |
|-------|---------|
| `requirements` | Functional requirements (REQ-XXX) |
| `nfr` | Non-functional requirements (NFR-XXX) |
| `project_state` | Current project state and workflow |
| `reuse_libraries` | Registered reuse library repos |
| `components` | Registered components |
| `component_dependencies` | Non-project-scope dependency catalog |
| `provisioning_jobs` | Provisioning job tracking |
| `provisioning_steps` | Job steps with compensation |
| `project_templates` | Data-driven project templates |
| `requirement_changes` | Audit trail |
| `prompt_segments` | Composable prompt segments for CLAUDE.md |
| `segment_compositions` | Variant-specific segment compositions |
| `composition_items` | Links segments to compositions with order |
| `segment_tags` | Flexible segment classification tags |

### Migration Commands
```bash
python db/migrate.py up       # Run pending migrations
python db/migrate.py down     # Rollback last migration
python db/migrate.py status   # Show migration status
python db/migrate.py reset    # Reset and re-run all
```

## Provisioning Components

### Mandatory Components

| Component | Purpose | Skip Override | Status |
|-----------|---------|---------------|--------|
| `bmad-method` | BMAD methodology framework | Yes (special circumstances) | **DEFINED** (REQ-019) |

**BMAD Installation Options:**
```yaml
bmad_method:
  enabled: true          # Mandatory default
  skip: false            # Override to skip
  headless: true         # Unattended mode
  variant: "default"     # rm-claude-code variant
```

### Optional Components

| Component | Purpose | Status |
|-----------|---------|--------|
| SQLite | Project-level database | **IMPLEMENTED** (REQ-017) |
| Other databases | TBD | Pending |
| Persistent storage | TBD | Pending |

## Test Environment

- **Test Project:** `~/repos/test-project`
- **Teardown:** Delete contents, preserve folder
- **Feature Flags:** Control remote provisioning tests

## Working Repositories

| Repository | Path | Purpose |
|------------|------|---------|
| self-improving-factory | `~/repos/self-improving-factory` | Main development |
| project-setup | `~/repos/project-setup` | Legacy extraction source |
| test-project | `~/repos/test-project` | E2E testing target |

## Memories

### Session Memories

- **User:** Roy
- **Agent:** Barry (Quick Flow Solo Dev)
- **BMAD Version:** 6.0.0-Beta.5

### Operational Memories

1. **Requirements Mode:** All requirements must be documented immediately with PRD format, traceability IDs, and TDD test criteria
2. **State Persistence:** Save state after every significant operation to `_bmad-output/`
3. **Legacy Extraction:** Use `discovery-catalog-project-setup-legacy.md` as reference for controlled extraction
4. **Test Control:** Use feature flags for remote provisioning tests to avoid issues during unit/E2E testing
5. **Incremental Input:** Accept requirements via prompts or docs/ folder text files
6. **Reuse Libraries:** System manages configurable number of software reuse libraries (repos created/managed by factory or descendants)
7. **Library-First Pattern (CRITICAL):** All new assets go to reuse libraries first (source of truth), then sync to projects idempotently
8. **Requirement Scope:** Unless otherwise noted, ALL requirements apply to both this project AND descendant projects

### Library-First Asset Management (REQ-021)

**CRITICAL OPERATIONAL PATTERN** - Apply to all asset development:

```
Asset Created → Infer Target Library → Write to Library → Sync to Project
```

| Asset Type | Target Library |
|------------|----------------|
| Python modules | `rm-python` |
| TypeScript modules | `rm-typescript` |
| Skills, Agents, Workflows | `rm-claude-code` |
| Templates, Hooks | `rm-claude-code` |
| CLAUDE.md variants | `rm-claude-code` |

**Sync Rules:**
- Libraries = Source of Truth (canonical)
- Copy to project idempotently (create if not exists, update if changed)
- Preserve project customizations during merge
- Flag conflicts for manual resolution
- Log all sync operations

### Reuse Libraries

| Library ID | Purpose | Status |
|------------|---------|--------|
| `rm-claude-code` | CLAUDE.md configuration variants with DAG catalogs | **DEFINED** (REQ-018) |
| `rm-python` | Python reusable modules | NOT YET DEFINED |
| `rm-typescript` | TypeScript reusable modules | NOT YET DEFINED |
| `rm-skills` | Reusable agentic skills/specifications | NOT YET DEFINED |

### rm-claude-code Library Structure

```
rm-claude-code/
├── variants/
│   ├── production-enterprise-grade/   # First variant (REQ-020)
│   │   ├── CLAUDE.md       # Root config (auto-loaded)
│   │   ├── DAG.md          # Dependency graph catalog
│   │   ├── skills/         # Lazy-load skills
│   │   ├── agents/         # Lazy-load agents
│   │   ├── workflows/      # Workflows
│   │   └── hooks/          # Event hooks
│   └── ...
└── shared/                 # Shared components
```

### Defined Variants

| Variant ID | Name | Use Case | Status |
|------------|------|----------|--------|
| `production-enterprise-grade` | Production Enterprise Grade | Enterprise systems, regulated industries | **DEFINED** (REQ-020) |

### Production Enterprise Grade Principles

| Principle | Enforcement |
|-----------|-------------|
| SOLID | Mandatory (5-pass validation) |
| TDD | Mandatory (Red-Green-Refactor) |
| DRY | Mandatory (reuse checks) |
| Security | Mandatory (OWASP, secrets) |
| Traceability | Mandatory (Req→Code→Test) |

**Quality Gates:** SOLID Review, Security Scan, Test Coverage (≥90%), Code Review, Compliance Check
