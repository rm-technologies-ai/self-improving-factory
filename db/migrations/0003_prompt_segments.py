"""
Prompt segments database for composable CLAUDE.md construction.

Supports:
- Prompt segment storage with classification
- Sequencing for ordered composition
- Variant-specific segments (e.g., production-enterprise-grade)
- Reusable segments across variants
"""

from datetime import datetime

NOW = datetime.utcnow().isoformat()


def up(conn):
    """Apply migration - create prompt segments tables."""

    # Main prompt segments table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prompt_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            content TEXT NOT NULL,

            -- Classification columns
            variant TEXT,
            section TEXT,
            category TEXT,
            subcategory TEXT,
            target_file TEXT DEFAULT 'CLAUDE.md',

            -- Sequencing
            sequence_order INTEGER DEFAULT 0,
            parent_segment_id TEXT,

            -- Metadata
            is_required INTEGER DEFAULT 0,
            is_conditional INTEGER DEFAULT 0,
            condition_expression TEXT,

            -- Versioning
            version TEXT DEFAULT '1.0.0',

            -- Timestamps
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY (parent_segment_id) REFERENCES prompt_segments(segment_id)
        )
    """)

    # Segment compositions - defines how segments combine for a variant
    conn.execute("""
        CREATE TABLE IF NOT EXISTS segment_compositions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            composition_id TEXT NOT NULL UNIQUE,
            variant TEXT NOT NULL,
            target_file TEXT DEFAULT 'CLAUDE.md',
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Composition items - links segments to compositions with order
    conn.execute("""
        CREATE TABLE IF NOT EXISTS composition_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            composition_id TEXT NOT NULL,
            segment_id TEXT NOT NULL,
            sequence_order INTEGER NOT NULL,
            is_enabled INTEGER DEFAULT 1,
            override_content TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (composition_id) REFERENCES segment_compositions(composition_id),
            FOREIGN KEY (segment_id) REFERENCES prompt_segments(segment_id),
            UNIQUE(composition_id, segment_id)
        )
    """)

    # Segment tags for flexible classification
    conn.execute("""
        CREATE TABLE IF NOT EXISTS segment_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (segment_id) REFERENCES prompt_segments(segment_id),
            UNIQUE(segment_id, tag)
        )
    """)

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_prompt_segments_variant ON prompt_segments(variant)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_prompt_segments_section ON prompt_segments(section)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_prompt_segments_category ON prompt_segments(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_prompt_segments_target ON prompt_segments(target_file)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_prompt_segments_sequence ON prompt_segments(sequence_order)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_composition_items_order ON composition_items(composition_id, sequence_order)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_segment_tags_tag ON segment_tags(tag)")

    conn.commit()
    print("    Created prompt_segments, segment_compositions, composition_items, segment_tags tables")

    # Create initial composition for production-enterprise-grade
    conn.execute("""
        INSERT INTO segment_compositions (composition_id, variant, target_file, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "claude-md-production-enterprise-grade",
        "production-enterprise-grade",
        "CLAUDE.md",
        "Production Enterprise Grade CLAUDE.md",
        "Composable CLAUDE.md for enterprise-grade projects with full engineering rigor",
        NOW, NOW
    ))

    conn.commit()
    print("    Created production-enterprise-grade composition")


def down(conn):
    """Rollback migration - drop prompt segment tables."""
    conn.execute("DROP TABLE IF EXISTS segment_tags")
    conn.execute("DROP TABLE IF EXISTS composition_items")
    conn.execute("DROP TABLE IF EXISTS segment_compositions")
    conn.execute("DROP TABLE IF EXISTS prompt_segments")
    conn.commit()
    print("    Dropped prompt segment tables")
