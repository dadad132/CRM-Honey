"""
Migration script to add billing/completion details columns to task table
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
    cursor.execute("PRAGMA table_info(task)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"Existing columns: {len(existing_columns)} columns")
    
    # New columns to add for billing/completion details
    new_columns = [
        ("billable_traveling", "VARCHAR"),
        ("billable_labour_onsite", "VARCHAR"),
        ("billable_remote_labour", "VARCHAR"),
        ("billable_equipment_used", "VARCHAR"),
        ("non_billable_traveling", "VARCHAR"),
        ("non_billable_labour_onsite", "VARCHAR"),
        ("non_billable_remote_labour", "VARCHAR"),
        ("non_billable_equipment_used", "VARCHAR"),
        ("completion_notes", "TEXT"),
    ]
    
    added = 0
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE task ADD COLUMN {col_name} {col_type}"
                print(f"Adding column: {col_name}")
                cursor.execute(sql)
                print(f"  ✓ Added {col_name}")
                added += 1
            except Exception as e:
                print(f"  ✗ Error adding {col_name}: {e}")
        else:
            print(f"  - Column {col_name} already exists")
    
    conn.commit()
    conn.close()
    print(f"\nMigration complete! Added {added} new columns.")

if __name__ == "__main__":
    migrate()
