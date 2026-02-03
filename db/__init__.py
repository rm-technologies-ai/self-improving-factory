"""
Database module for self-improving-factory.

Provides project-scope SQLite database access with:
- Connection management
- Query helpers
- CRUD operations for core entities
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / ".data" / "factory.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def dict_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert sqlite3.Row to dict."""
    return dict(zip(row.keys(), row))


# Requirements operations
def get_requirement(req_id: str) -> Optional[Dict[str, Any]]:
    """Get a requirement by ID."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM requirements WHERE req_id = ?", (req_id,))
    row = cursor.fetchone()
    conn.close()
    return dict_from_row(row) if row else None


def get_all_requirements(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all requirements, optionally filtered by status."""
    conn = get_connection()
    if status:
        cursor = conn.execute(
            "SELECT * FROM requirements WHERE status = ? ORDER BY req_id",
            (status,)
        )
    else:
        cursor = conn.execute("SELECT * FROM requirements ORDER BY req_id")
    rows = cursor.fetchall()
    conn.close()
    return [dict_from_row(row) for row in rows]


def add_requirement(
    req_id: str,
    title: str,
    description: str,
    req_type: str = "functional",
    priority: str = "MEDIUM",
    section: str = None,
    acceptance_criteria: str = None,
    tdd_test_criteria: str = None
) -> int:
    """Add a new requirement."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute("""
        INSERT INTO requirements (
            req_id, title, description, type, priority, section,
            acceptance_criteria, tdd_test_criteria, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'defined', ?, ?)
    """, (req_id, title, description, req_type, priority, section,
          acceptance_criteria, tdd_test_criteria, now, now))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def update_requirement_status(req_id: str, status: str) -> bool:
    """Update requirement status."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute(
        "UPDATE requirements SET status = ?, updated_at = ? WHERE req_id = ?",
        (status, now, req_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def get_next_req_id() -> str:
    """Get the next available requirement ID."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT req_id FROM requirements ORDER BY req_id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        num = int(row["req_id"].replace("REQ-", ""))
        return f"REQ-{num + 1:03d}"
    return "REQ-001"


# Project state operations
def get_project_state() -> Optional[Dict[str, Any]]:
    """Get current project state."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM project_state ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict_from_row(row) if row else None


def update_project_state(**kwargs) -> bool:
    """Update project state fields."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    kwargs["updated_at"] = now

    set_clause = ", ".join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())

    cursor = conn.execute(
        f"UPDATE project_state SET {set_clause} WHERE id = (SELECT MAX(id) FROM project_state)",
        values
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


# Reuse libraries operations
def get_reuse_libraries() -> List[Dict[str, Any]]:
    """Get all reuse libraries."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM reuse_libraries ORDER BY library_id")
    rows = cursor.fetchall()
    conn.close()
    return [dict_from_row(row) for row in rows]


def add_reuse_library(
    library_id: str,
    name: str,
    description: str = None,
    library_type: str = None
) -> int:
    """Add a new reuse library."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute("""
        INSERT INTO reuse_libraries (
            library_id, name, description, library_type, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, 'pending', ?, ?)
    """, (library_id, name, description, library_type, now, now))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


# Components operations
def get_components(scope: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all components, optionally filtered by scope."""
    conn = get_connection()
    if scope:
        cursor = conn.execute(
            "SELECT * FROM components WHERE scope = ? ORDER BY component_id",
            (scope,)
        )
    else:
        cursor = conn.execute("SELECT * FROM components ORDER BY component_id")
    rows = cursor.fetchall()
    conn.close()
    return [dict_from_row(row) for row in rows]


def register_component(
    component_id: str,
    name: str,
    description: str = None,
    component_type: str = None,
    scope: str = "project",
    is_optional: bool = False,
    install_path: str = None
) -> int:
    """Register a new component."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    cursor = conn.execute("""
        INSERT INTO components (
            component_id, name, description, component_type, scope,
            is_optional, is_enabled, install_path, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
    """, (component_id, name, description, component_type, scope,
          1 if is_optional else 0, install_path, now, now))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id
