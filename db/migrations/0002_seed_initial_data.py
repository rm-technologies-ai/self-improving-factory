"""
Seed initial data from current PRD state.

Populates:
- Current requirements (REQ-001 to REQ-017)
- Non-functional requirements (NFR-001 to NFR-004)
- Project state
- Planned reuse libraries
- SQLite component registration
"""

from datetime import datetime

NOW = datetime.utcnow().isoformat()


def up(conn):
    """Apply migration - seed initial data."""

    # Seed requirements
    requirements = [
        ("REQ-001", "Idempotent Operations", "All operations must be idempotent - repeatable without causing unintended side effects.", "functional", "CRITICAL", "defined", "Core Requirements"),
        ("REQ-002", "Compensation Logic", "All operations must have proper compensation logic to recover from errors.", "functional", "CRITICAL", "defined", "Core Requirements"),
        ("REQ-003", "Exception Handling", "Robust exception handling for autonomous error recovery.", "functional", "CRITICAL", "defined", "Core Requirements"),
        ("REQ-004", "Headless/Autonomous Operation", "System operates without human-in-the-loop for standard operations.", "functional", "HIGH", "defined", "Core Requirements"),
        ("REQ-005", "Data-Driven Component Templates", "User-defined component combinations as persistent configuration templates, reusable by project type.", "functional", "HIGH", "defined", "Core Requirements"),
        ("REQ-006", "State Persistence", "Immediate state persistence for session recovery and failure restoration.", "functional", "HIGH", "defined", "Core Requirements"),
        ("REQ-007", "Local Repository Creation", "Create local repository with proper structure.", "functional", "HIGH", "defined", "Initial Provisioning"),
        ("REQ-008", "Support Files Integration", "Generate and integrate support files (README, configs, etc.).", "functional", "HIGH", "defined", "Initial Provisioning"),
        ("REQ-009", "Git Integration", "Full Git integration including remote setup.", "functional", "HIGH", "defined", "Initial Provisioning"),
        ("REQ-010", "Data-Driven Component Installation", "Install components based on data-driven configuration.", "functional", "HIGH", "defined", "Initial Provisioning"),
        ("REQ-011", "Test Project Support", "Support for test project at ~/repos/test-project for development and E2E testing.", "functional", "HIGH", "defined", "Test Environment"),
        ("REQ-012", "Feature Flag Control", "Feature flags to control test execution scope.", "functional", "HIGH", "defined", "Test Environment"),
        ("REQ-013", "Incremental Requirements Capture", "Capture incremental requirements via prompts or docs folder.", "functional", "HIGH", "defined", "Requirements Management"),
        ("REQ-014", "Configurable Reuse Library Management", "The system manages a configurable number of software reuse libraries.", "functional", "HIGH", "defined", "Reuse Library Management"),
        ("REQ-015", "Reuse Library Types", "Initial reuse library types to be managed by the factory.", "functional", "HIGH", "defined", "Reuse Library Management"),
        ("REQ-016", "Project-Scope Installation Principle", "All components must install at project scope level for portability and self-containment.", "foundational", "CRITICAL", "defined", "Core Requirements"),
        ("REQ-017", "SQLite Project-Level Installation", "Optional provisioning component for installing SQLite at the project level.", "optional", "MEDIUM", "in_progress", "Optional Components"),
    ]

    for req_id, title, description, req_type, priority, status, section in requirements:
        conn.execute("""
            INSERT INTO requirements (req_id, title, description, type, priority, status, section, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (req_id, title, description, req_type, priority, status, section, NOW, NOW))

    print(f"    Seeded {len(requirements)} requirements")

    # Seed NFRs
    nfrs = [
        ("NFR-001", "Traceability", "All requirements must be traceable from definition through implementation to test.", "quality"),
        ("NFR-002", "Test-Driven Design", "All requirements must include TDD test criteria before implementation begins.", "quality"),
        ("NFR-003", "State Durability", "State must survive session termination and system failures.", "reliability"),
        ("NFR-004", "Graceful Degradation", "System should continue processing independent operations when one fails.", "reliability"),
    ]

    for nfr_id, title, description, category in nfrs:
        conn.execute("""
            INSERT INTO nfr (nfr_id, title, description, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nfr_id, title, description, category, NOW, NOW))

    print(f"    Seeded {len(nfrs)} NFRs")

    # Seed project state
    conn.execute("""
        INSERT INTO project_state (
            project_name, project_path, status, current_phase, current_step,
            next_step, operational_mode, last_agent, last_activity,
            recovery_point, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "self-improving-factory",
        "~/repos/self-improving-factory",
        "active",
        "requirements-capture",
        "sqlite-installation",
        "define-additional-requirements",
        "continuous-requirements-capture",
        "quick-flow-solo-dev (Barry)",
        "sqlite-setup",
        "post-sqlite-installation",
        NOW, NOW
    ))

    print("    Seeded project state")

    # Seed planned reuse libraries
    libraries = [
        ("rm-python", "Python Reuse Modules", "Python reusable modules library", "python", "pending"),
        ("rm-typescript", "TypeScript Reuse Modules", "TypeScript reusable modules library", "typescript", "pending"),
        ("rm-skills", "Skills Library", "Reusable agentic skills/specifications library", "skills", "pending"),
    ]

    for lib_id, name, description, lib_type, status in libraries:
        conn.execute("""
            INSERT INTO reuse_libraries (library_id, name, description, library_type, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (lib_id, name, description, lib_type, status, NOW, NOW))

    print(f"    Seeded {len(libraries)} reuse libraries")

    # Register SQLite as a component
    conn.execute("""
        INSERT INTO components (
            component_id, name, description, component_type, scope,
            is_optional, is_enabled, install_path, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "sqlite",
        "SQLite Database",
        "Project-level SQLite database for data persistence",
        "database",
        "project",
        1,  # is_optional
        1,  # is_enabled
        ".data/factory.db",
        NOW, NOW
    ))

    print("    Registered SQLite component")

    conn.commit()


def down(conn):
    """Rollback migration - remove seeded data."""
    conn.execute("DELETE FROM requirement_changes")
    conn.execute("DELETE FROM components WHERE component_id = 'sqlite'")
    conn.execute("DELETE FROM reuse_libraries")
    conn.execute("DELETE FROM project_state")
    conn.execute("DELETE FROM nfr")
    conn.execute("DELETE FROM requirements")
    conn.commit()
    print("    Removed all seeded data")
