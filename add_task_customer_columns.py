"""
Migration script to add customer info columns to the task table.
Run this on the server after deploying the code update.
"""
import sqlite3
import os

def migrate():
    # Find database
    db_path = os.environ.get('DATABASE_URL', 'data.db')
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing columns in task table
    cursor.execute("PRAGMA table_info(task)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    print(f"Existing columns in task table: {existing_columns}")
    
    # Columns to add
    columns_to_add = [
        ('customer_name', 'VARCHAR'),
        ('customer_surname', 'VARCHAR'),
        ('customer_email', 'VARCHAR'),
        ('customer_phone', 'VARCHAR'),
    ]
    
    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE task ADD COLUMN {col_name} {col_type}")
                print(f"✅ Added column: {col_name}")
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not add {col_name}: {e}")
        else:
            print(f"ℹ️ Column {col_name} already exists")
    
    conn.commit()
    conn.close()
    print("\n✅ Migration complete!")

if __name__ == '__main__':
    migrate()
