# PRD: Self-Improving Factory - Incremental Requirements

---
bmad_type: prd-incremental
bmad_version: 6.0.0-Beta.5
project_name: self-improving-factory
status: active
created: 2026-02-03
last_updated: 2026-02-03
version: 0.11.0
---

## Document Purpose

This is a **living PRD** that captures incremental requirements as they are provided by the user. Each requirement is documented with:
- Traceability ID
- TDD test criteria
- Acceptance criteria
- Implementation notes

## Requirement Scope

**IMPORTANT:** Unless otherwise noted, all requirements in this document apply to:

1. **This project** (self-improving-factory) - the factory itself
2. **Descendant projects** - all projects provisioned by this factory

Requirements are inherited by descendant projects during provisioning and enforced during updates.

---

## 1. Project Vision

**Self-Improving Factory** is a headless/autonomous project provisioning system that:
- Provisions new projects or repos autonomously
- Conducts initialization, maintenance, updates, and removals
- Operates in an idempotent and graceful manner
- Implements compensation logic and exception handling
- Recovers from errors and continues processing autonomously

---

## 2. Core Requirements (Initial)

### REQ-001: Idempotent Operations

**Status:** Defined
**Priority:** CRITICAL

**Description:**
All operations must be idempotent - repeatable without causing unintended side effects.

**Acceptance Criteria:**
- [ ] Running the same operation twice produces identical results
- [ ] No duplicate resources created on repeated execution
- [ ] State checks performed before any mutating operation

**TDD Test Criteria:**
```
TEST: Operation idempotency
GIVEN: An operation has been executed once
WHEN: The same operation is executed again
THEN: The system state remains unchanged
AND: No errors are raised
```

---

### REQ-002: Compensation Logic

**Status:** Defined
**Priority:** CRITICAL

**Description:**
All operations must have proper compensation logic to recover from errors.

**Acceptance Criteria:**
- [ ] Each operation has a defined rollback procedure
- [ ] Partial failures trigger compensation for completed steps
- [ ] Compensation actions are logged for audit

**TDD Test Criteria:**
```
TEST: Compensation on failure
GIVEN: An operation consisting of steps A, B, C
WHEN: Step B fails
THEN: Compensation for step A is executed
AND: System returns to pre-operation state
```

---

### REQ-003: Exception Handling

**Status:** Defined
**Priority:** CRITICAL

**Description:**
Robust exception handling for autonomous error recovery.

**Acceptance Criteria:**
- [ ] All exceptions are caught and categorized
- [ ] Recoverable errors trigger retry with backoff
- [ ] Non-recoverable errors trigger compensation
- [ ] Processing continues for independent operations

**TDD Test Criteria:**
```
TEST: Autonomous error recovery
GIVEN: A transient error occurs
WHEN: The system detects the error
THEN: Retry is attempted with exponential backoff
AND: Processing continues after max retries
```

---

### REQ-004: Headless/Autonomous Operation

**Status:** Defined
**Priority:** HIGH

**Description:**
System operates without human-in-the-loop for standard operations.

**Acceptance Criteria:**
- [ ] No interactive prompts during execution
- [ ] Configuration-driven behavior
- [ ] Logging sufficient for post-execution review

**TDD Test Criteria:**
```
TEST: Headless execution
GIVEN: A valid configuration
WHEN: Provisioning is triggered
THEN: Execution completes without user input
AND: All decisions are logged
```

---

### REQ-005: Data-Driven Component Templates

**Status:** Defined
**Priority:** HIGH

**Description:**
User-defined component combinations as persistent configuration templates, reusable by project type.

**Acceptance Criteria:**
- [ ] Templates defined in configuration format (YAML/JSON)
- [ ] Templates selectable by project type identifier
- [ ] Components can be added/removed via template modification

**TDD Test Criteria:**
```
TEST: Template-based provisioning
GIVEN: A project type with defined template
WHEN: Provisioning is triggered for that type
THEN: All template-defined components are installed
AND: Component configuration matches template spec
```

---

### REQ-006: State Persistence

**Status:** Defined
**Priority:** HIGH

**Description:**
Immediate state persistence for session recovery and failure restoration.

**Acceptance Criteria:**
- [ ] State saved after each significant operation
- [ ] State file includes recovery point information
- [ ] Session can be restored from persisted state

**TDD Test Criteria:**
```
TEST: State recovery
GIVEN: A session with persisted state
WHEN: A new session loads the state
THEN: Work can continue from the recovery point
AND: No data is lost
```

---

### REQ-016: Project-Scope Installation Principle

**Status:** Defined
**Priority:** CRITICAL
**Type:** Foundational Design Principle

**Description:**
All components for this project and provisioned descendants must install at the project scope level to be portable and self-contained at the repo level. When project-level installation is not feasible, the component must be cataloged and handled accordingly during idempotent provisioning of descendant instances.

**Acceptance Criteria:**
- [ ] All components default to project-scope installation
- [ ] Components are self-contained within the repository
- [ ] Repository is portable (can be cloned and run without global dependencies)
- [ ] Non-project-scope components are cataloged in a dependency manifest
- [ ] Idempotent provisioning handles non-project-scope dependencies gracefully
- [ ] Clear documentation for any external/system-level dependencies

**TDD Test Criteria:**
```
TEST: Project-scope installation
GIVEN: A component to be installed
WHEN: Installation is triggered
THEN: Component is installed within the project directory
AND: No global/system-level modifications are made

TEST: Non-project-scope dependency catalog
GIVEN: A component that cannot be installed at project scope
WHEN: The component is registered
THEN: It is added to the dependency manifest
AND: Manifest includes installation instructions
AND: Idempotent provisioning checks for its presence

TEST: Repository portability
GIVEN: A fully provisioned repository
WHEN: The repository is cloned to a new location
THEN: All project-scope components are functional
AND: Non-project-scope dependencies are clearly identified
```

**Implementation Notes:**
- Prefer vendoring, local installs, or container-based isolation
- Use `.local/`, `vendor/`, or language-specific local paths (e.g., `node_modules/`, `.venv/`)
- Catalog system dependencies in a manifest file (e.g., `DEPENDENCIES.md` or `system-deps.yaml`)

---

## 3. Initial Provisioning Requirements

### REQ-007: Local Repository Creation

**Status:** Defined
**Priority:** HIGH

**Description:**
Create local repository with proper structure.

**Acceptance Criteria:**
- [ ] Directory structure created per project type
- [ ] Git initialized (if not exists)
- [ ] .gitignore created with appropriate patterns

**TDD Test Criteria:**
```
TEST: Repository creation
GIVEN: A target directory path
WHEN: Repository creation is triggered
THEN: Directory structure matches project type template
AND: Git repository is initialized
```

---

### REQ-008: Support Files Integration

**Status:** Defined
**Priority:** HIGH

**Description:**
Generate and integrate support files (README, configs, etc.).

**Acceptance Criteria:**
- [ ] README.md generated with project metadata
- [ ] Configuration files generated from templates
- [ ] Support files use variable substitution

**TDD Test Criteria:**
```
TEST: Support file generation
GIVEN: Project metadata and template
WHEN: Support files are generated
THEN: Variables are substituted correctly
AND: Files are placed in correct locations
```

---

### REQ-009: Git Integration

**Status:** Defined
**Priority:** HIGH

**Description:**
Full Git integration including remote setup.

**Acceptance Criteria:**
- [ ] Remote origin configured (when enabled)
- [ ] Initial commit created
- [ ] Branch protection rules applied (when enabled)

**TDD Test Criteria:**
```
TEST: Git remote setup
GIVEN: A local repository and remote URL
WHEN: Git integration is triggered (with flag enabled)
THEN: Remote origin is configured
AND: Initial push succeeds
```

**Feature Flag:** `ENABLE_REMOTE_PROVISIONING_TESTS`

---

### REQ-010: Data-Driven Component Installation

**Status:** Defined
**Priority:** HIGH

**Description:**
Install components based on data-driven configuration.

**Acceptance Criteria:**
- [ ] Components installed per template specification
- [ ] Installation order respects dependencies
- [ ] Failed component installation triggers compensation

**TDD Test Criteria:**
```
TEST: Component installation
GIVEN: A template with components A, B (depends on A), C
WHEN: Installation is triggered
THEN: Components installed in order: A, B, C
AND: All components are functional
```

---

## 4. Test Environment Requirements

### REQ-011: Test Project Support

**Status:** Defined
**Priority:** HIGH

**Description:**
Support for test project at `~/repos/test-project` for development and E2E testing.

**Acceptance Criteria:**
- [ ] Test project path configurable
- [ ] Test project preserves git history
- [ ] Teardown cleans contents but preserves folder

**TDD Test Criteria:**
```
TEST: Test project teardown
GIVEN: A test project with contents
WHEN: Teardown is triggered
THEN: All contents are removed
AND: Project folder still exists
AND: Git folder preserved or recreated
```

---

### REQ-012: Feature Flag Control

**Status:** Defined
**Priority:** HIGH

**Description:**
Feature flags to control test execution scope.

**Acceptance Criteria:**
- [ ] Remote provisioning tests controlled by flag
- [ ] Flagged tests skip when flag is disabled
- [ ] Flag state is clearly logged

**TDD Test Criteria:**
```
TEST: Feature flag behavior
GIVEN: ENABLE_REMOTE_PROVISIONING_TESTS = false
WHEN: Remote provisioning test suite runs
THEN: Tests are skipped with clear message
AND: No remote operations are attempted
```

---

## 5. Requirements Management

### REQ-013: Incremental Requirements Capture

**Status:** Defined
**Priority:** HIGH

**Description:**
Capture incremental requirements via prompts or docs folder.

**Acceptance Criteria:**
- [ ] Requirements from prompts documented immediately
- [ ] Requirements from docs/ folder parsed and integrated
- [ ] Each requirement gets unique ID

**TDD Test Criteria:**
```
TEST: Requirement capture
GIVEN: A new requirement via user prompt
WHEN: Requirement is provided
THEN: Requirement is documented in PRD
AND: Unique ID is assigned
AND: TDD test criteria are defined
```

---

## 6. Optional Provisioning Components

### REQ-017: SQLite Project-Level Installation

**Status:** IMPLEMENTED
**Priority:** MEDIUM
**Type:** Optional Component

**Description:**
Optional provisioning component for installing SQLite at the project level. Other database types and persistent components will be defined in subsequent requirements.

**Acceptance Criteria:**
- [x] SQLite installation is optional (controlled by configuration)
- [x] SQLite is installed at project scope (not system-wide)
- [x] Database files stored within project directory (`.data/factory.db`)
- [x] Installation is idempotent (migrations system with tracking)
- [x] Compensation logic handles installation failures (down() functions)

**Implementation Details:**
- Database: `.data/factory.db`
- Migrations: `db/migrations/*.py`
- Migration runner: `db/migrate.py`
- Python module: `db/__init__.py`
- Tables: 10 (requirements, nfr, project_state, reuse_libraries, components, etc.)

**TDD Test Criteria:**
```
TEST: SQLite project-level installation
GIVEN: A project configuration with SQLite enabled
WHEN: Provisioning is triggered
THEN: SQLite is installed at project scope
AND: Database path is within project directory

TEST: SQLite installation idempotency
GIVEN: SQLite is already installed at project scope
WHEN: Provisioning is triggered again
THEN: No duplicate installation occurs
AND: Existing database files are preserved

TEST: SQLite optional skip
GIVEN: A project configuration with SQLite disabled
WHEN: Provisioning is triggered
THEN: SQLite installation is skipped
AND: No SQLite-related files are created
```

**Implementation Notes:**
- Consider using `sqlite3` Python package with local installation
- Database files should be in `.data/` or similar project-local directory
- Future: Other databases (PostgreSQL, etc.) will follow same project-scope pattern where feasible

**Future Extensions (To Be Defined):**
- Other database types
- Other persistent storage components
- Caching layers

---

## 7. Software Reuse Library Management

### REQ-014: Configurable Reuse Library Management

**Status:** Defined
**Priority:** HIGH

**Description:**
The system manages a configurable number of software reuse libraries. These are repositories created and managed by this project factory or any of its descendants.

**Acceptance Criteria:**
- [ ] Number of reuse libraries is configurable
- [ ] Each library is a separate repository
- [ ] Libraries can be created by this factory or descendant factories
- [ ] Library registry tracks all managed libraries

**TDD Test Criteria:**
```
TEST: Reuse library registry
GIVEN: A factory configuration with N reuse libraries defined
WHEN: The factory initializes
THEN: All N libraries are registered
AND: Each library is accessible by identifier
```

---

### REQ-015: Reuse Library Types

**Status:** Defined (Instances Pending)
**Priority:** HIGH

**Description:**
Initial reuse library types to be managed by the factory.

**Planned Libraries:**

| Library ID | Purpose | Status |
|------------|---------|--------|
| `rm-python` | Python reusable modules | NOT YET DEFINED |
| `rm-typescript` | TypeScript reusable modules | NOT YET DEFINED |
| `rm-skills` | Reusable agentic skills/specifications | NOT YET DEFINED |
| `rm-claude-code` | CLAUDE.md configuration variants with DAG catalogs | DEFINED (REQ-018) |

**Acceptance Criteria:**
- [ ] Each library type has defined schema
- [ ] Libraries are independently versionable
- [ ] Cross-library dependencies are tracked
- [ ] Library definitions stored in factory configuration

**TDD Test Criteria:**
```
TEST: Library type registration
GIVEN: A library type definition (e.g., rm-python)
WHEN: The library is registered with the factory
THEN: Library schema is validated
AND: Library is available for provisioning operations
AND: Library appears in factory inventory
```

**Implementation Note:** Library definitions will be provided in subsequent requirements. Do not implement until specifications are complete.

---

### REQ-018: rm-claude-code Reuse Library

**Status:** Defined
**Priority:** HIGH
**Type:** Reuse Library Definition

**Description:**
The `rm-claude-code` reuse library contains different CLAUDE.md configuration variants, each self-contained in separate folders. CLAUDE.md is the root of all Claude Code agentic specifications and is automatically loaded at the beginning of a new session. This file references additional agentic specifications (skills, agents, workflows) in a hierarchical fashion, which lazy-load by design.

**Core Concepts:**

1. **CLAUDE.md as Root** - Auto-loaded at session start, serves as entry point for all agentic behavior
2. **Configuration Variants** - Different CLAUDE.md configurations for different project types/purposes
3. **Hierarchical References** - CLAUDE.md references skills and other specs that lazy-load on demand
4. **DAG Catalog** - Each variant includes a Directed Acyclic Graph catalog of dependencies and references
5. **Consistency Checker** - DAG markup file ensures all agentic specifications are synchronized

**Library Structure:**

```
rm-claude-code/
├── README.md                    # Library documentation
├── variants/
│   ├── <variant-name>/
│   │   ├── CLAUDE.md            # Root configuration for this variant
│   │   ├── DAG.md               # Dependency graph catalog
│   │   ├── skills/              # Variant-specific skills (lazy-load)
│   │   ├── agents/              # Variant-specific agents (lazy-load)
│   │   └── workflows/           # Variant-specific workflows
│   └── ...
└── shared/                      # Shared components across variants
    ├── skills/
    ├── agents/
    └── templates/
```

**Acceptance Criteria:**
- [ ] Library repository created and registered
- [ ] Variant folder structure defined
- [ ] Each variant contains a CLAUDE.md root configuration
- [ ] Each variant contains a DAG.md dependency catalog
- [ ] DAG catalog schema defined for consistency checking
- [ ] Lazy-load references properly documented
- [ ] Consistency checker validates DAG against actual files

**TDD Test Criteria:**
```
TEST: Variant structure validation
GIVEN: A rm-claude-code variant folder
WHEN: The variant is loaded
THEN: CLAUDE.md exists and is valid
AND: DAG.md exists and is valid
AND: All DAG references resolve to actual files

TEST: DAG consistency check
GIVEN: A variant with DAG.md catalog
WHEN: Consistency check is triggered
THEN: All referenced skills exist
AND: All referenced agents exist
AND: No orphaned specifications detected
AND: Circular dependencies are flagged

TEST: Lazy-load reference resolution
GIVEN: A CLAUDE.md with skill references
WHEN: A skill is invoked
THEN: The skill is loaded from the correct path
AND: The skill's dependencies are also available
```

**DAG Catalog Schema (DAG.md):**
```yaml
variant: <variant-name>
version: <semver>
root: CLAUDE.md
dependencies:
  skills:
    - path: skills/<skill-name>/SKILL.md
      lazy_load: true
      depends_on: []
  agents:
    - path: agents/<agent-name>/AGENT.md
      lazy_load: true
      depends_on: [skills/<dep-skill>]
  workflows:
    - path: workflows/<workflow-name>.md
      lazy_load: true
      depends_on: []
checksum: <sha256 of all referenced files>
last_validated: <timestamp>
```

**Implementation Notes:**
- CLAUDE.md is the single source of truth for session initialization
- Skills are invoked via `/skill-name` syntax and lazy-loaded
- DAG.md is maintained manually or via tooling to ensure synchronization
- Consistency checks should run before provisioning and on-demand

---

### REQ-019: BMAD Method Installation Component

**Status:** Defined
**Priority:** HIGH
**Type:** Provisioning Component

**Description:**
The BMAD method is installed as a component during the project provisioning process. It is included as a **mandatory default component** with an optional override to skip for special circumstances. The system must maintain installation options for headless/unattended installation of the BMAD method.

**Upstream Installer:**

The BMAD method has its own official installer:
```bash
npx bmad-method install
# Or specific version:
npx bmad-method@6.0.0-Beta.5 install
```

**Repository:** https://github.com/bmad-code-org/BMAD-METHOD

**Current Limitation:** The upstream installer is **interactive only** - it requires user prompts via `@clack/prompts`. There is no built-in headless/non-interactive mode (as of v6.0.0-Beta.5).

**Component Characteristics:**

| Property | Value |
|----------|-------|
| Component ID | `bmad-method` |
| Default Behavior | **Mandatory** (installed by default) |
| Skip Override | Optional flag to skip installation |
| Installation Mode | Interactive (upstream) / Headless (via wrapper - REQ-024) |
| Upstream Command | `npx bmad-method install` |

**Installation Options:**

```yaml
bmad_method:
  enabled: true                    # Default: true (mandatory)
  skip: false                      # Override to skip installation
  version: "latest"                # Version to install (e.g., "6.0.0-Beta.5")
  headless: true                   # Use headless wrapper (REQ-024)
  config:
    user_name: "${PROJECT_OWNER}"
    communication_language: "English"
    output_folder: "${PROJECT_ROOT}/_bmad-output"
```

**Acceptance Criteria:**
- [ ] BMAD method installed by default during provisioning
- [ ] Skip override available via configuration flag
- [ ] Headless installation via wrapper (REQ-024) completes without user prompts
- [ ] Installation is idempotent (safe to run multiple times)
- [ ] BMAD version is configurable
- [ ] Installation logs all decisions for audit
- [ ] Compensation logic handles installation failures

**TDD Test Criteria:**
```
TEST: BMAD default installation
GIVEN: A project provisioning request with default config
WHEN: Provisioning is triggered
THEN: BMAD method is installed via npx bmad-method install
AND: _bmad folder structure is created
AND: .claude/commands/ contains BMAD slash commands

TEST: BMAD skip override
GIVEN: A project provisioning request with bmad_method.skip = true
WHEN: Provisioning is triggered
THEN: BMAD method installation is skipped
AND: Skip decision is logged
AND: No BMAD-related files are created

TEST: BMAD headless installation
GIVEN: A project provisioning request with bmad_method.headless = true
WHEN: Provisioning is triggered
THEN: Headless wrapper (REQ-024) is used
AND: Installation completes without user prompts
AND: All configuration values come from config file

TEST: BMAD installation idempotency
GIVEN: A project with BMAD already installed
WHEN: Provisioning is triggered again
THEN: Existing BMAD configuration is preserved
AND: No duplicate installations occur
AND: Version upgrades are handled gracefully (quick-update mode)

TEST: BMAD version pinning
GIVEN: A provisioning request with bmad_method.version = "6.0.0-Beta.5"
WHEN: Installation is triggered
THEN: Specific version is installed via npx bmad-method@6.0.0-Beta.5
```

**Headless Installation Parameters:**

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `version` | BMAD version to install | No | `latest` |
| `user_name` | User name for config | No | from env or `Developer` |
| `communication_language` | Language setting | No | `English` |
| `output_folder` | BMAD output folder path | No | `_bmad-output` |

**Special Circumstances for Skip:**
- Minimal/lightweight project configurations
- Projects using alternative methodology frameworks
- Test fixtures that don't require full BMAD
- Legacy project migrations (gradual adoption)

**Implementation Notes:**
- Uses upstream `npx bmad-method install` command
- Headless mode requires wrapper (REQ-024) due to interactive upstream installer
- Installation respects project-scope principle (REQ-016)
- Configuration stored in `_bmad/bmm/config.yaml`
- Skip override must be explicitly set (fail-safe default is install)
- CLAUDE.md variant (rm-claude-code) is deployed separately per REQ-023

---

### REQ-020: CLAUDE.md Variant - Production Enterprise Grade

**Status:** Defined
**Priority:** HIGH
**Type:** rm-claude-code Variant Definition

**Description:**
The "Production Enterprise Grade" variant is the first defined CLAUDE.md configuration type for the rm-claude-code library. This variant enforces rigorous software engineering standards suitable for production systems in enterprise environments.

**Variant Metadata:**

| Property | Value |
|----------|-------|
| Variant ID | `production-enterprise-grade` |
| Display Name | Production Enterprise Grade |
| Target Use Case | Production systems, enterprise environments |
| Rigor Level | Maximum |
| Default for | Enterprise projects, regulated industries |

**Engineering Principles Enforced:**

| Principle | Enforcement Level | Description |
|-----------|-------------------|-------------|
| **SOLID** | Mandatory | All 5 principles with validation passes |
| **TDD** | Mandatory | Red-Green-Refactor cycle enforced |
| **DRY** | Mandatory | Duplication detection and reuse checks |
| **Data-Driven** | Mandatory | Configuration over code |
| **Idempotency** | Mandatory | All operations repeatable |
| **Compensation Logic** | Mandatory | Rollback for all mutations |
| **Traceability** | Mandatory | Requirements → Code → Tests linkage |
| **Security** | Mandatory | OWASP, secrets protection, input validation |

**Variant File Structure:**

```
rm-claude-code/variants/production-enterprise-grade/
├── CLAUDE.md                    # Root configuration
├── DAG.md                       # Dependency graph catalog
├── skills/
│   ├── setup/SKILL.md           # Project initialization
│   ├── create-prd/SKILL.md      # PRD generation
│   ├── create-implementation/SKILL.md
│   ├── execute-implementation/SKILL.md
│   ├── code-review/SKILL.md     # Comprehensive code review
│   ├── security-audit/SKILL.md  # Security validation
│   └── compliance-check/SKILL.md # Regulatory compliance
├── agents/
│   ├── solid-reviewer/AGENT.md  # SOLID validation (5-pass)
│   ├── security-scanner/AGENT.md # Security analysis
│   ├── test-runner/AGENT.md     # TDD execution
│   └── reuse-analyzer/AGENT.md  # DRY/reuse detection
├── workflows/
│   ├── implementation-workflow.md
│   ├── review-workflow.md
│   └── release-workflow.md
├── templates/
│   ├── prd-template.md
│   ├── nfr-template.md
│   └── implementation-plan-template.md
└── hooks/
    ├── pre-commit/
    ├── post-write/
    └── validation/
```

**CLAUDE.md Sections (Production Enterprise Grade):**

```markdown
# CLAUDE.md - Production Enterprise Grade

## Project Overview
[Auto-populated from project config]

## Engineering Principles (MANDATORY)
- SOLID (5 principles, validation enforced)
- TDD (Red-Green-Refactor, coverage targets)
- DRY (Reuse library integration)
- Data-Driven (Configuration over code)
- Security First (OWASP, secrets management)

## Validation Checklists
[Pre-commit, pre-merge, pre-release gates]

## Skills Reference (Lazy-Load)
[Hierarchical skill references]

## Agents Reference (Lazy-Load)
[Specialized validation agents]

## Workflows
[Standard enterprise workflows]

## Quality Gates
[Mandatory gates before progression]

## Compliance
[Regulatory/audit requirements]
```

**DAG.md Catalog for this Variant:**

```yaml
variant: production-enterprise-grade
version: 1.0.0
root: CLAUDE.md
quality_tier: enterprise
enforcement: strict

dependencies:
  skills:
    - path: skills/setup/SKILL.md
      lazy_load: true
      required: true
    - path: skills/create-prd/SKILL.md
      lazy_load: true
      required: true
    - path: skills/create-implementation/SKILL.md
      lazy_load: true
      required: true
    - path: skills/execute-implementation/SKILL.md
      lazy_load: true
      required: true
    - path: skills/code-review/SKILL.md
      lazy_load: true
      required: true
    - path: skills/security-audit/SKILL.md
      lazy_load: true
      required: true
    - path: skills/compliance-check/SKILL.md
      lazy_load: true
      required: false

  agents:
    - path: agents/solid-reviewer/AGENT.md
      lazy_load: true
      invoked_by: [skills/execute-implementation, skills/code-review]
    - path: agents/security-scanner/AGENT.md
      lazy_load: true
      invoked_by: [skills/security-audit, skills/code-review]
    - path: agents/test-runner/AGENT.md
      lazy_load: true
      invoked_by: [skills/execute-implementation]
    - path: agents/reuse-analyzer/AGENT.md
      lazy_load: true
      invoked_by: [skills/execute-implementation]

  workflows:
    - path: workflows/implementation-workflow.md
      type: primary
    - path: workflows/review-workflow.md
      type: quality
    - path: workflows/release-workflow.md
      type: release

  hooks:
    - path: hooks/pre-commit/
      trigger: PreToolUse[Write,Edit]
    - path: hooks/post-write/
      trigger: PostToolUse[Write,Edit]
    - path: hooks/validation/
      trigger: OnDemand

validation:
  consistency_check: required
  orphan_detection: enabled
  circular_dependency_check: enabled

checksum: <sha256>
last_validated: <timestamp>
```

**Acceptance Criteria:**
- [ ] Variant folder structure created in rm-claude-code
- [ ] CLAUDE.md root configuration complete
- [ ] DAG.md catalog with all dependencies
- [ ] All mandatory skills defined
- [ ] All validation agents defined
- [ ] Hooks structure in place
- [ ] Quality gates documented
- [ ] Consistency checker validates variant

**TDD Test Criteria:**
```
TEST: Variant structure completeness
GIVEN: The production-enterprise-grade variant folder
WHEN: Structure validation is run
THEN: CLAUDE.md exists with all required sections
AND: DAG.md exists with valid schema
AND: All referenced skills exist
AND: All referenced agents exist

TEST: Enterprise enforcement validation
GIVEN: A project using production-enterprise-grade variant
WHEN: Code changes are made
THEN: SOLID validation runs (5 passes)
AND: TDD cycle is enforced
AND: Security checks are performed
AND: Quality gates block non-compliant code

TEST: DAG consistency for variant
GIVEN: The production-enterprise-grade DAG.md
WHEN: Consistency check runs
THEN: All file references resolve
AND: No orphaned specifications found
AND: No circular dependencies exist
```

**Quality Gates (Enterprise Grade):**

| Gate | Trigger | Blocking |
|------|---------|----------|
| SOLID Review | Pre-commit | Yes |
| Security Scan | Pre-commit | Yes |
| Test Coverage | Pre-merge | Yes (≥90%) |
| Code Review | Pre-merge | Yes |
| Compliance Check | Pre-release | Configurable |

---

### REQ-021: Library-First Asset Management Pattern

**Status:** Defined
**Priority:** CRITICAL
**Type:** Foundational Operational Pattern

**Description:**
Throughout project development, all new artifacts (code, skills, templates, agents, workflows) are automatically placed in the appropriate reuse library as the **source of truth**. Assets are then copied or updated to the current project (and descendant projects) in an idempotent fashion. Merging considerations are applied during provisioning and updates to maintain integrity.

**Core Pattern:**

```
┌─────────────────────────────────────────────────────────────┐
│                    REUSE LIBRARIES                          │
│              (Source of Truth)                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ rm-python    │ │rm-typescript │ │ rm-skills    │ ...    │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘        │
│         │                │                │                 │
│  ┌──────────────────────────────────────────────────┐      │
│  │              rm-claude-code                       │      │
│  │   (CLAUDE.md variants, DAGs, agentic specs)      │      │
│  └──────────────────────┬───────────────────────────┘      │
└─────────────────────────┼───────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            │ Idempotent  │   Merge     │
            │    Copy     │   Logic     │
            ▼             ▼             ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ self-improving-   │ │ descendant-       │ │ descendant-       │
│ factory           │ │ project-1         │ │ project-N         │
│ (this project)    │ │                   │ │                   │
└───────────────────┘ └───────────────────┘ └───────────────────┘
```

**Asset Placement Inference Rules:**

| Asset Type | Target Library | Inference Criteria |
|------------|----------------|-------------------|
| Python modules | `rm-python` | `.py` files, reusable utilities |
| TypeScript modules | `rm-typescript` | `.ts` files, reusable utilities |
| Skills (SKILL.md) | `rm-skills` or `rm-claude-code` | Agentic skill definitions |
| Agents (AGENT.md) | `rm-claude-code` | Subagent definitions |
| Workflows | `rm-claude-code` | Workflow specifications |
| Templates | `rm-claude-code` | Document/code templates |
| CLAUDE.md variants | `rm-claude-code` | Root configurations |
| DAG catalogs | `rm-claude-code` | Dependency graphs |
| Hooks | `rm-claude-code` | Event-driven scripts |

**Operational Flow:**

1. **Asset Creation**
   - New asset developed in context of current work
   - Auto-infer target reuse library based on asset type
   - Write asset to reuse library (source of truth)

2. **Project Synchronization**
   - Copy asset from library to current project
   - Apply idempotent write (create if not exists, update if changed)
   - Log synchronization action

3. **Descendant Provisioning**
   - During provisioning: copy from libraries to new project
   - During updates: merge with existing project assets
   - Preserve project-specific customizations

4. **Merge Considerations**

   | Scenario | Strategy |
   |----------|----------|
   | New file | Direct copy |
   | File unchanged | Skip (idempotent) |
   | Library updated, project unchanged | Update from library |
   | Project customized | Merge with conflict detection |
   | Both changed | Flag for manual resolution |

**Acceptance Criteria:**
- [ ] Asset type inference rules implemented
- [ ] Reuse library placement automatic
- [ ] Libraries are source of truth (canonical)
- [ ] Idempotent copy to current project works
- [ ] Idempotent copy to descendant projects works
- [ ] Merge logic handles all scenarios
- [ ] Customizations preserved during updates
- [ ] Conflicts detected and flagged
- [ ] All operations logged for audit

**TDD Test Criteria:**
```
TEST: Asset type inference
GIVEN: A new skill file (SKILL.md)
WHEN: Asset placement is inferred
THEN: Target library is rm-skills or rm-claude-code
AND: Asset is written to library first

TEST: Idempotent copy to project
GIVEN: An asset exists in reuse library
WHEN: Sync to project is triggered
THEN: Asset is copied if not exists
AND: Asset is updated if library version is newer
AND: No action if identical (idempotent)

TEST: Merge with customization preservation
GIVEN: A project asset with local customizations
WHEN: Library asset is updated
THEN: Merge is attempted
AND: Customizations are preserved
AND: Conflicts are flagged if detected

TEST: Descendant project provisioning
GIVEN: A new descendant project being provisioned
WHEN: Assets are copied from libraries
THEN: All required assets are copied
AND: Project-specific config is applied
AND: Operation is idempotent on re-run
```

**Integrity Guarantees:**

| Guarantee | Implementation |
|-----------|----------------|
| Single source of truth | Libraries are canonical |
| No data loss | Merge preserves customizations |
| Idempotency | Same operation = same result |
| Auditability | All sync operations logged |
| Conflict visibility | Merge conflicts flagged |

**Implementation Notes:**
- Asset writes go to library first, then sync to project
- Use checksums to detect changes
- Maintain sync manifest per project (tracks library versions)
- Conflict resolution defaults to preserve local, flag for review
- This pattern applies to both initial provisioning and updates

---

### REQ-022: Prompt Segments Database

**Status:** IMPLEMENTED
**Priority:** HIGH
**Type:** Data Infrastructure

**Description:**
The system maintains a database of prompt segments with classification columns for composable CLAUDE.md construction. Segments can be sequenced, categorized, and combined into variant-specific compositions. First use case: define prompt segments for the production-enterprise-grade installation type.

**Database Schema:**

```
prompt_segments
├── segment_id (unique identifier)
├── name, description
├── content (the prompt text)
├── Classification:
│   ├── variant (e.g., production-enterprise-grade)
│   ├── section (e.g., principles, skills, workflows)
│   ├── category (e.g., engineering, security, quality)
│   ├── subcategory
│   └── target_file (default: CLAUDE.md)
├── Sequencing:
│   ├── sequence_order
│   └── parent_segment_id
├── Metadata:
│   ├── is_required
│   ├── is_conditional
│   └── condition_expression
└── version, timestamps

segment_compositions
├── composition_id
├── variant
├── target_file
└── name, description

composition_items
├── composition_id
├── segment_id
├── sequence_order
├── is_enabled
└── override_content

segment_tags
├── segment_id
└── tag
```

**Use Cases:**

1. **CLAUDE.md Composition** - Assemble CLAUDE.md from ordered segments
2. **Variant Management** - Different segment sets per variant
3. **Segment Reuse** - Share segments across variants
4. **Conditional Inclusion** - Include segments based on conditions
5. **Override Support** - Override segment content per composition

**Acceptance Criteria:**
- [x] prompt_segments table created
- [x] segment_compositions table created
- [x] composition_items table created
- [x] segment_tags table created
- [x] Indexes for efficient queries
- [x] production-enterprise-grade composition initialized
- [ ] Segments for production-enterprise-grade defined

**TDD Test Criteria:**
```
TEST: Segment storage and retrieval
GIVEN: A prompt segment with classification
WHEN: Stored in database
THEN: Segment retrievable by id, variant, section, category

TEST: Composition assembly
GIVEN: A composition with multiple segments
WHEN: Composition is assembled
THEN: Segments are returned in sequence order
AND: Disabled segments are excluded
AND: Overrides are applied

TEST: Segment reuse across variants
GIVEN: A segment used in multiple compositions
WHEN: Segment is updated
THEN: All compositions reflect the update
AND: Overrides are preserved
```

**Implementation Status:**
- Migration: `db/migrations/0003_prompt_segments.py`
- Tables: 4 created (prompt_segments, segment_compositions, composition_items, segment_tags)
- Indexes: 7 created for query optimization
- Initial composition: `claude-md-production-enterprise-grade` created

---

### REQ-023: CLAUDE.md Deployment to Descendant Projects

**Status:** Defined
**Priority:** HIGH
**Type:** Provisioning Operation

**Description:**
During project provisioning, the system deploys the appropriate CLAUDE.md variant to descendant projects based on the provisioning configuration. The CLAUDE.md is composed from prompt segments in the library (source of truth) and deployed idempotently to the target project.

**Deployment Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Provisioning Command                      │
│   provision --variant=production-enterprise-grade            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    rm-claude-code Library                    │
│   1. Load composition for variant                            │
│   2. Assemble segments in sequence order                     │
│   3. Apply any project-specific overrides                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Target Project                            │
│   4. Deploy CLAUDE.md (idempotent write)                     │
│   5. Deploy CLAUDE-ADD.md template (if not exists)           │
│   6. Log deployment for audit                                │
└─────────────────────────────────────────────────────────────┘
```

**Configuration Options:**

```yaml
provisioning:
  claude_md:
    variant: "production-enterprise-grade"  # Required
    deploy: true                            # Default: true
    overwrite_existing: false               # Default: false (preserve customizations)
    deploy_claude_add: true                 # Deploy CLAUDE-ADD.md template
    project_overrides:                      # Optional project-specific overrides
      project_name: "${PROJECT_NAME}"
      additional_memories: []
```

**Variant Selection:**

| Variant ID | Use Case | Rigor Level |
|------------|----------|-------------|
| `production-enterprise-grade` | Enterprise production systems | Maximum |
| `standard` | General purpose projects | Medium |
| `minimal` | Lightweight/experimental | Low |

**Deployment Behavior:**

| Scenario | Action |
|----------|--------|
| CLAUDE.md not exists | Deploy from library |
| CLAUDE.md exists, overwrite=false | Skip, preserve existing |
| CLAUDE.md exists, overwrite=true | Replace with library version |
| CLAUDE-ADD.md not exists | Deploy template |
| CLAUDE-ADD.md exists | Skip (always preserve customizations) |

**Acceptance Criteria:**
- [ ] Variant selection via provisioning configuration
- [ ] CLAUDE.md composed from library segments
- [ ] Idempotent deployment (safe to re-run)
- [ ] Existing CLAUDE.md preserved by default
- [ ] CLAUDE-ADD.md template deployed for project extensions
- [ ] Project-specific overrides supported
- [ ] Deployment logged for audit
- [ ] Rollback supported on failure

**TDD Test Criteria:**
```
TEST: CLAUDE.md deployment with variant selection
GIVEN: A provisioning request with variant=production-enterprise-grade
WHEN: Provisioning is triggered
THEN: CLAUDE.md is composed from library segments
AND: CLAUDE.md is deployed to target project
AND: Deployment is logged

TEST: Idempotent deployment (existing file preservation)
GIVEN: A target project with existing CLAUDE.md
AND: overwrite_existing=false
WHEN: Provisioning is triggered
THEN: Existing CLAUDE.md is preserved
AND: No overwrite occurs
AND: Skip is logged

TEST: CLAUDE-ADD.md template deployment
GIVEN: A target project without CLAUDE-ADD.md
WHEN: Provisioning is triggered with deploy_claude_add=true
THEN: CLAUDE-ADD.md template is deployed
AND: Template includes placeholder sections

TEST: Project-specific overrides
GIVEN: A provisioning request with project_overrides
WHEN: CLAUDE.md is composed
THEN: Override values are substituted
AND: Project name is populated
AND: Additional memories are included

TEST: Deployment rollback on failure
GIVEN: A deployment that fails mid-operation
WHEN: Compensation is triggered
THEN: Partial deployment is rolled back
AND: Original state is restored
```

**Implementation Notes:**
- Composition uses `lib-claude-md-peg` or equivalent library asset
- Library is source of truth (REQ-021)
- Respects project-scope installation principle (REQ-016)
- CLAUDE-ADD.md is never overwritten (project customizations are sacred)
- Deployment tracked in provisioning_steps table

---

### REQ-024: Headless BMAD Installation Wrapper

**Status:** IMPLEMENTED
**Priority:** HIGH
**Type:** Tooling Component

**Description:**
The upstream BMAD installer (`npx bmad-method install`) is interactive and requires user prompts. This requirement defines a headless wrapper that enables unattended BMAD installation for autonomous provisioning workflows.

**Problem Statement:**
- Upstream BMAD installer uses `@clack/prompts` for interactive configuration
- No built-in `--headless` or `--non-interactive` flag exists
- Autonomous provisioning requires non-interactive installation

**Solution Approaches:**

| Approach | Pros | Cons |
|----------|------|------|
| **Expect Script Wrapper** | Works with current upstream | Brittle if prompts change |
| **Upstream PR** | Clean solution | Dependency on upstream acceptance |
| **Direct File Copy** | Simple, predictable | Misses installer logic, updates |
| **Mock stdin** | No external deps | Complex, may break |

**Recommended Approach:** Expect Script Wrapper (short-term) + Upstream PR (long-term)

**Wrapper Specification:**

```bash
# Usage
bmad-headless-install [options]

# Options
--version <version>     # BMAD version (default: latest)
--user-name <name>      # User name for config
--language <lang>       # Communication language (default: English)
--output-dir <path>     # Output folder (default: _bmad-output)
--modules <list>        # Modules to install (comma-separated)
--skip-agents           # Skip agent compilation
--debug                 # Enable debug output
```

**Wrapper Implementation (Python with pexpect):**

```python
import pexpect
import sys

def install_bmad_headless(
    version: str = "latest",
    user_name: str = "Developer",
    language: str = "English",
    output_dir: str = "_bmad-output",
    modules: list = None,
    timeout: int = 120
) -> bool:
    """
    Install BMAD method non-interactively.

    Uses pexpect to automate the interactive installer prompts.
    """
    cmd = f"npx bmad-method@{version} install"
    child = pexpect.spawn(cmd, timeout=timeout)

    # Handle prompts based on expected sequence
    # (Prompt patterns to be determined from installer)

    child.expect(pexpect.EOF)
    return child.exitstatus == 0
```

**Acceptance Criteria:**
- [ ] Wrapper installs BMAD without user interaction
- [ ] All configuration options passable via CLI flags
- [ ] Works with pinned BMAD versions
- [ ] Handles installer updates gracefully (version detection)
- [ ] Logs all automated responses for audit
- [ ] Fails cleanly if prompt sequence changes
- [ ] Compensation logic for failed installations

**TDD Test Criteria:**
```
TEST: Headless installation basic
GIVEN: A target directory and default config
WHEN: bmad-headless-install is executed
THEN: BMAD is installed without prompts
AND: _bmad/ structure is created
AND: .claude/commands/ contains slash commands

TEST: Headless installation with options
GIVEN: Custom user_name, language, and output_dir
WHEN: bmad-headless-install --user-name "Roy" --language "English" --output-dir "_custom"
THEN: Configuration reflects provided options
AND: Output directory matches specified path

TEST: Version pinning
GIVEN: A specific BMAD version requirement
WHEN: bmad-headless-install --version "6.0.0-Beta.5"
THEN: Exactly that version is installed
AND: Version is logged for audit

TEST: Installer prompt change detection
GIVEN: BMAD installer has changed prompt sequence
WHEN: bmad-headless-install runs
THEN: Failure is detected and reported
AND: Clear error message indicates prompt mismatch
AND: No partial installation left behind

TEST: Idempotent reinstallation
GIVEN: BMAD already installed in target
WHEN: bmad-headless-install is executed
THEN: Quick-update mode is triggered
AND: Existing configuration is preserved
```

**Dependencies:**
- Python 3.10+
- pexpect (for expect-style automation)
- Node.js 20+ (for npx)

**Integration Points:**
- Called by provisioning orchestrator (REQ-010)
- Used before CLAUDE.md deployment (REQ-023)
- Respects project-scope installation (REQ-016)

**Future Consideration:**
Submit PR to upstream BMAD-METHOD for native `--headless` flag support.

---

### REQ-025: Interactive Provisioning CLI

**Status:** Defined
**Priority:** HIGH
**Type:** User Interface Component

**Description:**
The system provides a user-friendly interactive CLI to provision new projects or update existing ones. The installer dynamically presents options from data-driven configuration steps and proceeds to provision or update the target descendant repository. The interface is colorful, friendly, and provides recommended defaults pre-selected for quick setup.

**UX Design Principles:**

| Principle | Implementation |
|-----------|----------------|
| **Colorful** | Rich terminal colors, emoji indicators, styled boxes |
| **Friendly** | Welcoming messages, clear instructions, helpful hints |
| **Smart Defaults** | Recommended options pre-selected, one-key acceptance |
| **Progressive** | Show only relevant options, hide complexity |
| **Forgiving** | Easy to go back, clear undo/cancel options |

**CLI Entry Point:**

```bash
# Provision new project
sif provision [target-path]

# Update existing project
sif update [target-path]

# Interactive mode (default)
sif
```

**User Experience Flow:**

```
╭──────────────────────────────────────────────────────────────╮
│                                                              │
│   🏭  Self-Improving Factory  v0.1.0                         │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                     │
│                                                              │
│   Welcome! Let's set up your project.                        │
│                                                              │
│   What would you like to do?                                 │
│                                                              │
│   ● Provision new project  (Recommended)                     │
│   ○ Update existing project                                  │
│   ○ Manage reuse libraries                                   │
│   ○ Exit                                                     │
│                                                              │
│   ↑/↓ Navigate  ⏎ Select  q Quit                            │
│                                                              │
╰──────────────────────────────────────────────────────────────╯
```

**Color Scheme:**

| Element | Color | Purpose |
|---------|-------|---------|
| Headers/Titles | Cyan/Bold | Visual hierarchy |
| Selected option | Green + ● | Clear selection state |
| Recommended | Yellow badge | Guide user to best choice |
| Success messages | Green | Positive feedback |
| Warnings | Yellow | Attention needed |
| Errors | Red | Problems to address |
| Hints/Help | Dim/Gray | Secondary information |
| Progress | Blue/Cyan | Activity indication |

**Data-Driven Steps:**

The installer dynamically loads available options from:

| Source | Provides |
|--------|----------|
| `project_templates` table | Project type templates |
| `components` table | Available components |
| `reuse_libraries` table | Library options |
| `prompt_segments` table | CLAUDE.md variants |
| Configuration files | Environment-specific settings |

**Provisioning Flow (with Smart Defaults):**

```
1. Select Operation
   └─> ● Provision (default) / ○ Update

2. Target Selection
   └─> 📁 Enter path: ~/repos/my-project
   └─> 💡 Hint: Directory will be created if it doesn't exist

3. Project Type (data-driven, default pre-selected)
   └─> ● Python (Recommended)
   └─> ○ TypeScript
   └─> ○ Claude Code Project
   └─> ○ Custom

4. CLAUDE.md Variant (data-driven, default pre-selected)
   └─> ● production-enterprise-grade (Recommended)
   └─> ○ standard
   └─> ○ minimal

5. Components (recommended defaults pre-checked)
   └─> ✅ BMAD Method (Required)
   └─> ✅ SQLite Database (Recommended)
   └─> ✅ GitHub Actions (Recommended)
   └─> ☐ Docker Support
   └─> 💡 Press ⏎ to accept defaults, or customize

6. Configuration (smart defaults from environment)
   └─> Project name: my-project (from path)
   └─> Author: Roy (from git config)
   └─> License: MIT (default)
   └─> 💡 Press ⏎ to accept all defaults

7. Confirmation (visual summary)
   ╭─────────────────────────────────────╮
   │ 📋 Review Your Selections           │
   ├─────────────────────────────────────┤
   │ Path:     ~/repos/my-project        │
   │ Type:     Python                    │
   │ Variant:  production-enterprise     │
   │ Components: BMAD, SQLite, Actions   │
   ╰─────────────────────────────────────╯
   └─> ● Confirm & Create / ○ Go Back / ○ Cancel

8. Execution (animated progress)
   └─> ⠋ Creating directory structure...
   └─> ✓ Directory created
   └─> ⠋ Installing BMAD Method...
   └─> ✓ BMAD installed
   └─> ⠋ Deploying CLAUDE.md...
   └─> ✓ Complete!
```

**Default Selection Rules:**

| Step | Default | Rationale |
|------|---------|-----------|
| Operation | Provision | Most common action |
| Project Type | Python | Most versatile |
| CLAUDE.md Variant | production-enterprise-grade | Maximum quality |
| BMAD Method | Required (locked) | Core functionality |
| SQLite | Pre-selected | State management |
| GitHub Actions | Pre-selected | CI/CD best practice |
| Author | From `git config user.name` | Auto-detect |
| License | MIT | Permissive default |

**Update Flow:**

```
1. Select Target Project
   └─> Browse / Enter path

2. Detect Current State
   └─> Read project configuration
   └─> Identify installed components
   └─> Check versions

3. Update Options (data-driven)
   └─> [ ] Update CLAUDE.md variant
   └─> [ ] Add components
   └─> [ ] Update BMAD Method
   └─> [ ] Sync from libraries

4. Preview Changes
   └─> Show what will change
   └─> Highlight conflicts

5. Confirmation
   └─> Review, confirm

6. Execution
   └─> Idempotent updates
   └─> Preserve customizations
```

**UI Components (using @clack/prompts style):**

```python
# Example using Python inquirer/rich
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress

console = Console()

# Selection prompt
project_type = Prompt.ask(
    "Project type",
    choices=load_project_types(),  # Data-driven
    default="python"
)

# Multi-select
components = inquirer.checkbox(
    message="Select components",
    choices=load_available_components(),  # Data-driven
)

# Progress display
with Progress() as progress:
    task = progress.add_task("Provisioning...", total=len(steps))
    for step in steps:
        execute_step(step)
        progress.advance(task)
```

**Acceptance Criteria:**
- [ ] Interactive CLI launches with `sif` command
- [ ] **Colorful UI** with rich terminal colors and emoji indicators
- [ ] **Friendly messaging** with welcoming tone and helpful hints
- [ ] **Smart defaults pre-selected** for quick one-key acceptance
- [ ] Recommended options marked with "(Recommended)" badge
- [ ] Options dynamically loaded from database/config
- [ ] Project types loaded from `project_templates` table
- [ ] Components loaded from `components` table
- [ ] CLAUDE.md variants loaded from `prompt_segments` table
- [ ] Clear progress indication with animated spinners
- [ ] Graceful error handling with compensation
- [ ] Update mode detects existing project state
- [ ] Customizations preserved during updates
- [ ] Visual confirmation summary before execution
- [ ] Headless mode available (--yes flag)
- [ ] Keyboard navigation hints displayed

**TDD Test Criteria:**
```
TEST: Interactive provisioning flow
GIVEN: User runs `sif provision`
WHEN: User selects project type, components, and confirms
THEN: Project is provisioned with selected options
AND: All selected components are installed
AND: Progress is displayed throughout

TEST: Data-driven option loading
GIVEN: Database contains project templates
WHEN: Provisioning wizard starts
THEN: All templates appear as selectable options
AND: Options are loaded dynamically

TEST: Update existing project
GIVEN: An existing provisioned project
WHEN: User runs `sif update <path>`
THEN: Current state is detected
AND: Update options are presented
AND: Customizations are preserved

TEST: Headless provisioning
GIVEN: A configuration file with all options
WHEN: User runs `sif provision --config config.yaml --yes`
THEN: Provisioning completes without prompts
AND: All options from config are applied

TEST: Compensation on failure
GIVEN: Provisioning in progress
WHEN: A step fails
THEN: Previous steps are compensated
AND: User is notified of failure
AND: System returns to clean state

TEST: Colorful UI rendering
GIVEN: User runs `sif` in a color-capable terminal
WHEN: The wizard displays
THEN: Headers are rendered in cyan/bold
AND: Selected options are highlighted in green
AND: Recommended badges are displayed in yellow
AND: Progress spinners are animated

TEST: Smart defaults pre-selected
GIVEN: User starts provisioning wizard
WHEN: Each step is displayed
THEN: Recommended option is pre-selected (●)
AND: User can press Enter to accept default
AND: "(Recommended)" badge is visible

TEST: One-key default acceptance
GIVEN: User is on a step with smart defaults
WHEN: User presses Enter without changing selection
THEN: Default values are accepted
AND: Wizard proceeds to next step
AND: Entire flow can complete with Enter-only navigation
```

**CLI Options:**

```bash
sif [command] [options]

Commands:
  provision [path]     Provision new project
  update [path]        Update existing project
  list-templates       Show available project templates
  list-components      Show available components

Options:
  --config <file>      Use configuration file
  --yes, -y            Skip confirmation prompts
  --dry-run            Show what would be done
  --verbose, -v        Verbose output
  --version            Show version
  --help, -h           Show help
```

**Dependencies:**
- Python 3.10+
- rich (terminal UI)
- inquirer or questionary (prompts)
- click or typer (CLI framework)

**Implementation Notes:**
- CLI is the primary user interface for the factory
- All options are data-driven (no hardcoded choices)
- Supports both interactive and headless modes
- Integrates with REQ-024 (headless BMAD wrapper) for BMAD installation
- Uses database tables as source of truth for options
- Progress display uses spinner and step indicators

---

## 8. Non-Functional Requirements (NFR)

### NFR-001: Traceability

**Description:** All requirements must be traceable from definition through implementation to test.

### NFR-002: Test-Driven Design

**Description:** All requirements must include TDD test criteria before implementation begins.

### NFR-003: State Durability

**Description:** State must survive session termination and system failures.

### NFR-004: Graceful Degradation

**Description:** System should continue processing independent operations when one fails.

---

## 9. Requirement Change Log

| Date | Req ID | Change | Author |
|------|--------|--------|--------|
| 2026-02-03 | REQ-001 to REQ-013 | Initial requirements from project brief | Roy |
| 2026-02-03 | NFR-001 to NFR-004 | Initial NFRs defined | Roy |
| 2026-02-03 | REQ-014, REQ-015 | Software Reuse Library Management requirements | Roy |
| 2026-02-03 | REQ-016 | Project-Scope Installation Principle (foundational) | Roy |
| 2026-02-03 | REQ-017 | SQLite Project-Level Installation (optional component) | Roy |
| 2026-02-03 | REQ-017 | SQLite IMPLEMENTED - database, migrations, schema ready | Barry |
| 2026-02-03 | REQ-018 | rm-claude-code Reuse Library defined (CLAUDE.md variants + DAG catalogs) | Roy |
| 2026-02-03 | REQ-019 | BMAD Method Installation Component (mandatory default, headless support) | Roy |
| 2026-02-03 | REQ-020 | CLAUDE.md Variant: Production Enterprise Grade defined | Roy |
| 2026-02-03 | REQ-021 | Library-First Asset Management Pattern (CRITICAL operational pattern) | Roy |
| 2026-02-03 | REQ-022 | Prompt Segments Database IMPLEMENTED (composable CLAUDE.md) | Roy/Barry |
| 2026-02-03 | REQ-023 | CLAUDE.md Deployment to Descendant Projects | Roy |
| 2026-02-03 | REQ-019 | Updated: BMAD uses upstream installer (npx bmad-method install) | Roy |
| 2026-02-03 | REQ-024 | Headless BMAD Installation Wrapper | Roy |
| 2026-02-03 | REQ-025 | Interactive Provisioning CLI | Roy |

---

## 10. Pending Requirements

*This section captures requirements that need clarification or are in discussion.*

(None currently)

---

## Document Footer

```yaml
created_by: Barry (Quick Flow Solo Dev)
maintained_by: Barry (Quick Flow Solo Dev)
created_at: 2026-02-03
last_updated: 2026-02-03
version: 0.11.0
status: active
change_log:
  - "0.1.0: Initial requirements (REQ-001 to REQ-013, NFR-001 to NFR-004)"
  - "0.2.0: Added Software Reuse Library Management (REQ-014, REQ-015)"
  - "0.3.0: Added Project-Scope Installation Principle (REQ-016) and SQLite Optional Component (REQ-017)"
  - "0.4.0: Added rm-claude-code Reuse Library definition (REQ-018)"
  - "0.5.0: Added BMAD Method Installation Component (REQ-019)"
  - "0.6.0: Added Production Enterprise Grade variant (REQ-020)"
  - "0.7.0: Added Library-First Asset Management Pattern (REQ-021)"
  - "0.8.0: Added Prompt Segments Database IMPLEMENTED (REQ-022)"
  - "0.9.0: Added CLAUDE.md Deployment to Descendant Projects (REQ-023)"
  - "0.10.0: Updated REQ-019 for upstream BMAD installer, added Headless Wrapper (REQ-024)"
  - "0.11.0: Added Interactive Provisioning CLI (REQ-025)"
  - "0.9.0: Added CLAUDE.md Deployment to Descendant Projects (REQ-023)"
```
