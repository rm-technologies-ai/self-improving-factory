#!/usr/bin/env python3
"""
Database Migration Runner

Project-scope SQLite migration system for self-improving-factory.
Supports idempotent migrations with compensation logic.

Usage:
    python db/migrate.py [command]

Commands:
    up      - Run all pending migrations (default)
    down    - Rollback last migration
    status  - Show migration status
    reset   - Rollback all and re-run (destructive)
"""

import sqlite3
import os
import sys
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / ".data" / "factory.db"
MIGRATIONS_DIR = PROJECT_ROOT / "db" / "migrations"


def get_connection() -> sqlite3.Connection:
    """Get database connection, creating .data directory if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_migrations_table(conn: sqlite3.Connection) -> None:
    """Create migrations tracking table if not exists (idempotent)."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            checksum TEXT
        )
    """)
    conn.commit()


def get_applied_migrations(conn: sqlite3.Connection) -> List[str]:
    """Get list of applied migration versions."""
    cursor = conn.execute("SELECT version FROM _migrations ORDER BY version")
    return [row["version"] for row in cursor.fetchall()]


def get_pending_migrations() -> List[Tuple[str, str, Path]]:
    """Get list of pending migration files (version, name, path)."""
    migrations = []
    if MIGRATIONS_DIR.exists():
        for f in sorted(MIGRATIONS_DIR.glob("*.py")):
            if f.name.startswith("_"):
                continue
            # Expected format: NNNN_name.py
            parts = f.stem.split("_", 1)
            if len(parts) == 2:
                version, name = parts
                migrations.append((version, name, f))
    return migrations


def load_migration(path: Path):
    """Dynamically load a migration module."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_migration_up(conn: sqlite3.Connection, version: str, name: str, path: Path) -> bool:
    """Run a single migration's up() function."""
    try:
        module = load_migration(path)
        if hasattr(module, "up"):
            print(f"  Running migration {version}_{name}...")
            module.up(conn)
            conn.execute(
                "INSERT INTO _migrations (version, name, applied_at) VALUES (?, ?, ?)",
                (version, name, datetime.utcnow().isoformat())
            )
            conn.commit()
            print(f"  [OK] {version}_{name} applied")
            return True
        else:
            print(f"  [SKIP] {version}_{name} has no up() function")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [FAIL] {version}_{name}: {e}")
        return False


def run_migration_down(conn: sqlite3.Connection, version: str, name: str, path: Path) -> bool:
    """Run a single migration's down() function (compensation)."""
    try:
        module = load_migration(path)
        if hasattr(module, "down"):
            print(f"  Rolling back migration {version}_{name}...")
            module.down(conn)
            conn.execute("DELETE FROM _migrations WHERE version = ?", (version,))
            conn.commit()
            print(f"  [OK] {version}_{name} rolled back")
            return True
        else:
            print(f"  [SKIP] {version}_{name} has no down() function (no compensation)")
            return False
    except Exception as e:
        conn.rollback()
        print(f"  [FAIL] {version}_{name} rollback: {e}")
        return False


def cmd_up() -> int:
    """Run all pending migrations."""
    conn = get_connection()
    ensure_migrations_table(conn)

    applied = set(get_applied_migrations(conn))
    pending = get_pending_migrations()

    to_apply = [(v, n, p) for v, n, p in pending if v not in applied]

    if not to_apply:
        print("No pending migrations.")
        return 0

    print(f"Running {len(to_apply)} migration(s)...")
    success_count = 0
    for version, name, path in to_apply:
        if run_migration_up(conn, version, name, path):
            success_count += 1
        else:
            print(f"Migration failed. Stopping.")
            break

    print(f"\n{success_count}/{len(to_apply)} migrations applied.")
    conn.close()
    return 0 if success_count == len(to_apply) else 1


def cmd_down() -> int:
    """Rollback the last applied migration."""
    conn = get_connection()
    ensure_migrations_table(conn)

    applied = get_applied_migrations(conn)
    if not applied:
        print("No migrations to rollback.")
        return 0

    last_version = applied[-1]
    pending = get_pending_migrations()

    for version, name, path in pending:
        if version == last_version:
            run_migration_down(conn, version, name, path)
            break
    else:
        print(f"Migration file for {last_version} not found.")
        return 1

    conn.close()
    return 0


def cmd_status() -> int:
    """Show migration status."""
    conn = get_connection()
    ensure_migrations_table(conn)

    applied = set(get_applied_migrations(conn))
    pending = get_pending_migrations()

    print(f"Database: {DB_PATH}")
    print(f"Migrations directory: {MIGRATIONS_DIR}")
    print()

    if not pending:
        print("No migrations found.")
        return 0

    print("Migration Status:")
    print("-" * 60)
    for version, name, path in pending:
        status = "[APPLIED]" if version in applied else "[PENDING]"
        print(f"  {status} {version}_{name}")

    applied_count = len([v for v, _, _ in pending if v in applied])
    pending_count = len(pending) - applied_count
    print("-" * 60)
    print(f"Applied: {applied_count}, Pending: {pending_count}")

    conn.close()
    return 0


def cmd_reset() -> int:
    """Reset database - rollback all and re-run."""
    print("WARNING: This will reset the database!")

    conn = get_connection()
    ensure_migrations_table(conn)

    applied = get_applied_migrations(conn)
    pending = get_pending_migrations()

    # Rollback in reverse order
    print(f"Rolling back {len(applied)} migration(s)...")
    for version in reversed(applied):
        for v, name, path in pending:
            if v == version:
                run_migration_down(conn, version, name, path)
                break

    conn.close()

    # Re-run all
    print("\nRe-running all migrations...")
    return cmd_up()


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "up"

    commands = {
        "up": cmd_up,
        "down": cmd_down,
        "status": cmd_status,
        "reset": cmd_reset,
    }

    if command in commands:
        sys.exit(commands[command]())
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
