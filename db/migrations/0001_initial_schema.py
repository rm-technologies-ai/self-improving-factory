"""
Initial schema for self-improving-factory.

Creates core tables for:
- Requirements tracking (functional and non-functional)
- Project state management
- Reuse library registry
- Component management
- Provisioning job tracking
- Dependency catalog (for non-project-scope components)
"""


def up(conn):
    """Apply migration - create initial schema."""

    # Requirements table (REQ-XXX entries)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            req_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'functional',
            priority TEXT DEFAULT 'MEDIUM',
            status TEXT DEFAULT 'defined',
            section TEXT,
            acceptance_criteria TEXT,
            tdd_test_criteria TEXT,
            implementation_notes TEXT,
            feature_flag TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Non-functional requirements table (NFR-XXX entries)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS nfr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nfr_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            status TEXT DEFAULT 'defined',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Project state table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS project_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            project_path TEXT NOT NULL,
            status TEXT DEFAULT 'initialized',
            current_phase TEXT,
            current_step TEXT,
            next_step TEXT,
            operational_mode TEXT,
            last_agent TEXT,
            last_activity TEXT,
            last_artifact TEXT,
            recovery_point TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Reuse libraries registry
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reuse_libraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            library_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            library_type TEXT,
            repo_path TEXT,
            repo_url TEXT,
            status TEXT DEFAULT 'pending',
            schema_version TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Components registry
    conn.execute("""
        CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            component_type TEXT,
            scope TEXT DEFAULT 'project',
            is_optional INTEGER DEFAULT 0,
            is_enabled INTEGER DEFAULT 1,
            install_path TEXT,
            config_schema TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Component dependencies (for non-project-scope components per REQ-016)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS component_dependencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id TEXT NOT NULL,
            dependency_name TEXT NOT NULL,
            dependency_type TEXT,
            scope TEXT DEFAULT 'system',
            version_constraint TEXT,
            install_instructions TEXT,
            check_command TEXT,
            is_satisfied INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (component_id) REFERENCES components(component_id)
        )
    """)

    # Provisioning jobs tracking
    conn.execute("""
        CREATE TABLE IF NOT EXISTS provisioning_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL UNIQUE,
            job_type TEXT NOT NULL,
            target_project TEXT,
            target_path TEXT,
            status TEXT DEFAULT 'pending',
            config TEXT,
            started_at TEXT,
            completed_at TEXT,
            error_message TEXT,
            compensation_status TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Provisioning job steps (for compensation logic)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS provisioning_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            step_number INTEGER NOT NULL,
            step_name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            started_at TEXT,
            completed_at TEXT,
            error_message TEXT,
            compensation_action TEXT,
            compensation_status TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES provisioning_jobs(job_id)
        )
    """)

    # Project templates (for data-driven component combinations)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS project_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            project_type TEXT,
            components TEXT,
            config_defaults TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Change log for requirements (audit trail)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requirement_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            req_id TEXT NOT NULL,
            change_type TEXT NOT NULL,
            change_description TEXT,
            author TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Create indexes for common queries
    conn.execute("CREATE INDEX IF NOT EXISTS idx_requirements_status ON requirements(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_requirements_priority ON requirements(priority)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_provisioning_jobs_status ON provisioning_jobs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_provisioning_steps_job_id ON provisioning_steps(job_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_reuse_libraries_status ON reuse_libraries(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_components_scope ON components(scope)")

    conn.commit()
    print("    Created 10 tables with indexes")


def down(conn):
    """Rollback migration - drop all tables (compensation)."""
    tables = [
        "requirement_changes",
        "project_templates",
        "provisioning_steps",
        "provisioning_jobs",
        "component_dependencies",
        "components",
        "reuse_libraries",
        "project_state",
        "nfr",
        "requirements",
    ]

    for table in tables:
        conn.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()
    print(f"    Dropped {len(tables)} tables")
