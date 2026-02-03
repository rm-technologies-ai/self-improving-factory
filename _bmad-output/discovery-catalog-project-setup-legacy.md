# Discovery Catalog: project-setup (Legacy)

---
bmad_type: discovery-catalog
bmad_version: 6.0.0-Beta.5
source_project: project-setup
source_path: ~/repos/project-setup
target_project: self-improving-factory
discovery_date: 2026-02-03
status: complete
---

## BMAD Reflection Metadata

```yaml
artifact_purpose: Legacy codebase distillation reference
extraction_status: pending
integration_priority: high
dependencies: []
blockers: []
next_actions:
  - Extract core 4-skill MVP workflow specifications
  - Distill hook scripts for idempotent operations
  - Adapt DAG architecture for headless provisioning
  - Create compensation logic framework from existing patterns
related_workflows:
  - quick-spec
  - quick-dev
tags:
  - legacy-extraction
  - architecture-reference
  - skill-specifications
  - agent-definitions
```

---

## Executive Summary

**project-setup** is a production-grade provisioning accelerator for Claude Code projects. It implements a **4-skill MVP workflow** with lazy-loaded agentic specifications, comprehensive validation infrastructure (SOLID/DRY/TDD), and self-improving feedback loops.

| Metric | Value |
|--------|-------|
| Total Files | ~106 specification and implementation files |
| Primary Language | Markdown, Bash, JSON (configuration-as-code) |
| Architecture | Lazy-load DAG with two-layer structure |
| Skills | 18 total (4 primary, 11 utility, 3 validators) |
| Agents | 3 (solid-reviewer, test-runner, reuse-analyzer) |

---

## 1. Directory Structure Overview

```
project-setup/
├── .claude/                          # Agentic specifications
│   ├── DAG.md                        # Lazy-load hierarchy
│   ├── dag-registry.json             # Component integrity validation
│   ├── project-config.md             # Project settings
│   ├── settings.json                 # Claude Code settings
│   ├── skills/                       # 18 skill definitions
│   ├── agents/                       # 3 subagent definitions
│   ├── workflows/                    # 4 workflow specifications
│   ├── templates/                    # 6 document templates
│   ├── hooks/                        # Event-driven scripts
│   ├── mcp/                          # MCP server configurations
│   ├── context/                      # Session persistence
│   └── scaffolding/                  # NEW PROJECT TEMPLATES
├── Root Documentation (CLAUDE.md, README.md, TASKS.md, backlog.md)
├── prds/                             # Product Requirements Documents
├── implementation-plans/             # Example implementation plans
├── aisrl-code-analysis/              # Engineering patterns reference
├── scripts/                          # Executable scripts
├── tests/                            # Test infrastructure
├── docs/claude-code/                 # Claude Code documentation
└── references/                       # PRD references
```

---

## 2. Agentic Specifications Catalog

### 2.1 Primary Skills (4-Skill MVP)

| Skill | Path | Purpose | Complexity | Extraction Priority |
|-------|------|---------|------------|---------------------|
| **setup** | `.claude/skills/setup/SKILL.md` | Initialize new projects with full scaffolding | HIGH | **CRITICAL** |
| **create-prd** | `.claude/skills/create-prd/SKILL.md` | Generate PRD + NFR with SOLID/DRY/TDD lens | HIGH | HIGH |
| **create-implementation** | `.claude/skills/create-implementation/SKILL.md` | Break down PRD into phased implementation plan | HIGH | HIGH |
| **execute-implementation** | `.claude/skills/execute-implementation/SKILL.md` | Execute plan with TDD + SOLID validation | VERY HIGH | **CRITICAL** |

### 2.2 Utility Skills

| Skill | Purpose | Extraction Priority |
|-------|---------|---------------------|
| save-context | Persist session state | MEDIUM |
| load-context | Resume from saved context | MEDIUM |
| new-task | Add task to TASKS.md (Ralph Loop) | HIGH |
| new-backlog | Add item to backlog.md | LOW |
| sync-dag | Validate DAG integrity | HIGH |
| update-setup | Apply configuration changes | MEDIUM |
| create-issue | GitHub issue creation | LOW |
| work-issue | Issue execution workflow | LOW |

### 2.3 Validation Skills

| Skill | Purpose | Extraction Priority |
|-------|---------|---------------------|
| solid-validator | SOLID principles enforcement (5 passes) | **CRITICAL** |
| dry-checker | DRY violation detection | HIGH |
| tdd-runner | TDD workflow execution | HIGH |
| reuse-checker | Reuse opportunity detection | MEDIUM |

### 2.4 Subagents

| Agent | Path | Purpose | Model | Extraction Priority |
|-------|------|---------|-------|---------------------|
| **solid-reviewer** | `.claude/agents/solid-reviewer/AGENT.md` | 5-pass SOLID validation | Sonnet | **CRITICAL** |
| **test-runner** | `.claude/agents/test-runner/AGENT.md` | TDD workflow executor | Opus | HIGH |
| **reuse-analyzer** | `.claude/agents/reuse-analyzer/AGENT.md` | Reuse opportunity detection | Haiku | MEDIUM |

---

## 3. Programmatic Executables Catalog

### 3.1 Hook Scripts

| Script | Path | Purpose | Lines | Extraction Priority |
|--------|------|---------|-------|---------------------|
| **auto-format.sh** | `.claude/hooks/scripts/` | Post-write auto-formatting | 44 | HIGH |
| **protect-files.sh** | `.claude/hooks/scripts/` | Pre-write protection | 38 | **CRITICAL** |
| **load-context.sh** | `.claude/hooks/scripts/` | SessionStart context loading | - | MEDIUM |
| **update-status.sh** | `.claude/hooks/scripts/` | PostToolUse status updates | - | LOW |
| **validate-dag.sh** | `.claude/hooks/scripts/` | DAG integrity validation | - | HIGH |

### 3.2 Project Scripts

| Script | Path | Purpose | Extraction Priority |
|--------|------|---------|---------------------|
| hello.sh | `scripts/hello.sh` | Demo script | LOW |
| test_hello.sh | `tests/test_hello.sh` | Bash test suite (3 tests) | MEDIUM |

---

## 4. Configuration Files Catalog

### 4.1 JSON Configurations

| File | Purpose | Lines | Extraction Priority |
|------|---------|-------|---------------------|
| **dag-registry.json** | DAG component registry | 305 | HIGH |
| **settings.json** | Claude Code settings | 62 | HIGH |
| **hooks.json** | Hook definitions | 64 | **CRITICAL** |
| **mcp/servers.json** | MCP server configurations | 59 | MEDIUM |
| **orchestrator-config.json** | Workflow orchestration | - | MEDIUM |

### 4.2 Environment Configuration

| File | Purpose | Extraction Priority |
|------|---------|---------------------|
| **.env.example** | Environment template (50 lines) | HIGH |
| **.gitignore** | Git exclusion rules (46 lines) | MEDIUM |

---

## 5. Documentation Catalog

### 5.1 Primary Documentation

| Document | Purpose | Lines | Extraction Priority |
|----------|---------|-------|---------------------|
| **CLAUDE.md** | Engineering principles + validation checklists | 217 | **CRITICAL** |
| **README.md** | Project overview | 151 | MEDIUM |
| **initial.md** | Project vision and requirements | ~240 | LOW |
| **TASKS.md** | Ralph Loop task registry | 53 | HIGH |
| **backlog.md** | Feature requests template | 40 | LOW |

### 5.2 Engineering Patterns Reference

| Document | Path | Coverage | Extraction Priority |
|----------|------|----------|---------------------|
| **aisrl-engineering-patterns.md** | `aisrl-code-analysis/` | Comprehensive patterns | HIGH |
| **01-repository-structure.md** | `aisrl-code-analysis/` | Layer model | MEDIUM |
| **02-solid-patterns.md** | `aisrl-code-analysis/` | SOLID patterns | HIGH |
| **03-tdd-patterns.md** | `aisrl-code-analysis/` | TDD infrastructure | HIGH |
| **04-dry-patterns.md** | `aisrl-code-analysis/` | DRY patterns | MEDIUM |
| **05-data-driven-patterns.md** | `aisrl-code-analysis/` | Data-driven patterns | MEDIUM |

### 5.3 Templates

| Template | Purpose | Extraction Priority |
|----------|---------|---------------------|
| **prd-template.md** | PRD generation scaffold | HIGH |
| **nfr-template.md** | Non-Functional Requirements | MEDIUM |
| **implementation-plan-template.md** | Implementation scaffold | HIGH |
| **implementation-status-template.md** | Task status tracking | MEDIUM |
| **context-template.md** | Session persistence | MEDIUM |
| **tasks-template.md** | TASKS.md row template | MEDIUM |

---

## 6. Architecture Patterns for Extraction

### 6.1 Lazy-Load DAG Pattern

**Purpose:** Efficient context management by loading only what's needed

**Key Concepts:**
- Always Loaded: CLAUDE.md (engineering principles)
- On-Demand: Skills, agents, templates loaded when invoked
- Scaffolding: Loaded only by `/setup` skill

**Source File:** `.claude/DAG.md` (260 lines)

### 6.2 Two-Layer Architecture

**Live Files:** Active project configuration
**Scaffolding Templates:** Copied to new projects with variable substitution

**Variables:** `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{DATE}}`, `{{SETUP_VERSION}}`

### 6.3 4-Skill MVP Workflow

```
/setup (Initialize)
   ↓
/create-prd (Requirements → PRD + NFR)
   ↓
/create-implementation (PRD → Plan)
   ↓
/execute-implementation (Plan → Code with validation)
```

### 6.4 Validation Loop (per task)

1. TDD Red (write failing test)
2. TDD Green (minimal code to pass)
3. SOLID 5-pass validation
4. DRY check (reuse opportunities)
5. Data-driven validation
6. TDD Refactor
7. CI/CD execution
8. Auto-merge on success

### 6.5 Ralph Loop Pattern

**Purpose:** Sequential task execution with status progression

**Status Symbols:** ⏳ (pending), 🔄 (in progress), ✅ (completed), ❌ (failed), ⛔ (aborted)

---

## 7. Reusability Assessment Matrix

### High Reusability (Extract First)

| Component | Path | Reason |
|-----------|------|--------|
| 4-Skill Workflow | `.claude/skills/` | Complete orchestration template |
| Scaffolding Templates | `.claude/scaffolding/` | Bootstrap for all projects |
| SOLID Validator Agent | `.claude/agents/solid-reviewer/` | Extensible validation |
| Hook Scripts | `.claude/hooks/scripts/` | Auto-formatting and protection |
| Engineering Patterns | `aisrl-code-analysis/` | Reference patterns |

### Medium Reusability (Adapt)

| Component | Path | Reason |
|-----------|------|--------|
| Project Config | `.claude/project-config.md` | Per-project customization |
| DAG Registry | `.claude/dag-registry.json` | Extensible schema |
| MCP Configurations | `.claude/mcp/servers.json` | Tool integrations |
| Workflow Definitions | `.claude/workflows/` | Process templates |

### Low Reusability (Reference Only)

| Component | Path | Reason |
|-----------|------|--------|
| Project-Specific Docs | `initial.md`, `TASKS.md` | Instance-specific |
| PRD/Implementation Plans | `prds/`, `implementation-plans/` | Project artifacts |
| Context Files | `.claude/context/` | Session ephemeral |

---

## 8. Key Patterns for Self-Improving Factory

### 8.1 Idempotent Operations

All setup operations are idempotent:
- File creation: Create if not exists, skip if exists
- File editing: Append or merge based on context
- Directory creation: Create if not exists
- Configuration: Merge with existing, preserve customizations

### 8.2 Compensation Logic Patterns

From hook scripts:
- Pre-validation before destructive operations
- Rollback capability via context snapshots
- Protected file patterns for safety

### 8.3 Self-Improving Feedback Loop

- Feature requests → backlog.md
- Reusable code → aisrl/backlog.md
- HITM decision points for human-in-the-loop

---

## 9. Extraction Roadmap

### Phase 1: Foundation (Critical)

1. Extract CLAUDE.md engineering principles
2. Extract protect-files.sh hook for safety
3. Extract hooks.json configuration pattern
4. Extract solid-validator skill framework

### Phase 2: Core Workflow

1. Extract setup skill (adapt for headless operation)
2. Extract execute-implementation skill (core execution loop)
3. Extract DAG architecture for lazy-loading

### Phase 3: Validation Infrastructure

1. Extract SOLID reviewer agent
2. Extract TDD runner agent
3. Extract dry-checker skill

### Phase 4: Templates and Scaffolding

1. Extract template system with variable substitution
2. Extract scaffolding MANIFEST pattern
3. Adapt for data-driven component templates

---

## 10. Integration Notes for self-improving-factory

### Requirements Alignment

| Legacy Feature | New Requirement | Adaptation Needed |
|----------------|-----------------|-------------------|
| Interactive setup | Headless/autonomous operation | Remove HITM, add config-driven defaults |
| Manual component selection | Data-driven component templates | Create template registry |
| Single-project focus | Multi-project provisioning | Add project registry |
| Manual teardown | Controlled teardown with flag | Add teardown skill with compensation |
| Session persistence | Cross-session state recovery | Enhance context system |

### Test Project Integration

- Test project: `~/repos/test-project` (git initialized, pushed to GitHub)
- Teardown: Delete contents, preserve folder
- Feature flags: Control remote provisioning tests

### State Persistence Requirements

- Store state immediately in `_bmad-output`
- Enable session recovery from failure state
- Support incremental requirements via prompts or docs folder

---

## Document Footer

```yaml
created_by: Barry (Quick Flow Solo Dev)
created_at: 2026-02-03
last_updated: 2026-02-03
version: 1.0.0
status: complete
next_review: on-demand
```
