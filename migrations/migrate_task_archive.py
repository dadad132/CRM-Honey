"""
Add task archiving fields to Task table
"""
import sqlite3
import os


def migrate():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data.db')
    if not os.path.exists(db_path):
        db_path = 'data.db'
    if not os.path.exists(db_path):
        print("  ⚠ data.db not found — skipping")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Adding task archiving fields to Task table...")

    try:
        cursor.execute("PRAGMA table_info(task)")
        columns = [row[1] for row in cursor.fetchall()]
        if not columns:
            print("  ⚠ task table does not exist yet — skipping")
            return

        for col_name, col_def in [
            ('is_archived', 'BOOLEAN DEFAULT 0'),
            ('archived_at', 'DATETIME DEFAULT NULL'),
        ]:
            if col_name not in columns:
                cursor.execute(f"ALTER TABLE task ADD COLUMN {col_name} {col_def}")
                print(f"  ✓ {col_name} column added")
            else:
                print(f"  ✓ {col_name} column already exists")

        cursor.execute("CREATE INDEX IF NOT EXISTS ix_task_is_archived ON task (is_archived)")
        conn.commit()
        print("✓ Migration completed successfully!")

    except Exception as e:
        print(f"  ⚠ Migration warning: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()
