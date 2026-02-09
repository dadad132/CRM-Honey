"""
Migration script to add completion notification columns to email_settings table
"""
import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'data.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(emailsettings)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"Existing columns: {existing_columns}")
    
    # New columns to add
    new_columns = [
        ("completion_notify_enabled", "BOOLEAN DEFAULT 0"),
        ("completion_notify_email", "VARCHAR"),
        ("completion_notify_task", "BOOLEAN DEFAULT 1"),
        ("completion_notify_ticket", "BOOLEAN DEFAULT 1"),
        ("completion_email_subject", "VARCHAR DEFAULT '{type} Completed - {title}'"),
        ("completion_email_body", "TEXT"),
    ]
    
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE emailsettings ADD COLUMN {col_name} {col_type}"
                print(f"Adding column: {col_name}")
                cursor.execute(sql)
                print(f"  ✓ Added {col_name}")
            except Exception as e:
                print(f"  ✗ Error adding {col_name}: {e}")
        else:
            print(f"  - Column {col_name} already exists")
    
    conn.commit()
    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    migrate()
