#!/usr/bin/env python3
"""
Fix missing database columns - adds all missing columns to existing database
"""
import sqlite3
import sys
from pathlib import Path

def add_column_if_not_exists(cursor, table, column, column_type, default_value=None):
    """Add a column to a table if it doesn't exist"""
    try:
        # Check if column exists
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        
        if column not in columns:
            # Add the column
            default_clause = f" DEFAULT {default_value}" if default_value is not None else ""
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}{default_clause}")
            print(f"✅ Added {table}.{column}")
            return True
        else:
            print(f"⏭️  {table}.{column} already exists")
            return False
    except Exception as e:
        print(f"❌ Error adding {table}.{column}: {e}")
        return False

def create_table_if_not_exists(cursor, table_name, create_sql):
    """Create a table if it doesn't exist"""
    try:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone():
            print(f"⏭️  Table '{table_name}' already exists")
            return False
        else:
            cursor.execute(create_sql)
            print(f"✅ Created table '{table_name}'")
            return True
    except Exception as e:
        print(f"❌ Error creating table {table_name}: {e}")
        return False

def main():
    db_path = Path("data.db")
    
    if not db_path.exists():
        print("❌ Database file not found: data.db")
        sys.exit(1)
    
    print("=" * 60)
    print("Fixing Missing Database Columns and Tables")
    print("=" * 60)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    changes_made = False
    
    # User table - missing columns
    print("\n📋 Checking 'user' table...")
    changes_made |= add_column_if_not_exists(cursor, "user", "calendar_color", "VARCHAR", "'#3b82f6'")
    changes_made |= add_column_if_not_exists(cursor, "user", "can_see_all_tickets", "BOOLEAN", "0")
    changes_made |= add_column_if_not_exists(cursor, "user", "google_id", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "user", "google_access_token", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "user", "google_refresh_token", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "user", "google_token_expiry", "DATETIME", "NULL")
    
    # Project table - missing columns
    print("\n📋 Checking 'project' table...")
    changes_made |= add_column_if_not_exists(cursor, "project", "support_email", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "imap_host", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "imap_port", "INTEGER", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "imap_username", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "imap_password", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "imap_use_ssl", "BOOLEAN", "1")
    changes_made |= add_column_if_not_exists(cursor, "project", "is_archived", "BOOLEAN", "0")
    changes_made |= add_column_if_not_exists(cursor, "project", "archived_at", "DATETIME", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "start_date", "DATE", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "project", "due_date", "DATE", "NULL")
    
    # Task table - missing columns
    print("\n📋 Checking 'task' table...")
    changes_made |= add_column_if_not_exists(cursor, "task", "is_archived", "BOOLEAN", "0")
    changes_made |= add_column_if_not_exists(cursor, "task", "archived_at", "DATETIME", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "task", "parent_task_id", "INTEGER", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "task", "working_days", "VARCHAR", "'0,1,2,3,4'")
    
    # Ticket table - missing columns
    print("\n📋 Checking 'ticket' table...")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "is_archived", "BOOLEAN", "0")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "archived_at", "DATETIME", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "closed_by_id", "INTEGER", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "is_guest", "BOOLEAN", "0")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_name", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_surname", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_email", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_phone", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_company", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_office_number", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "guest_branch", "VARCHAR", "NULL")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "working_days", "VARCHAR", "'0,1,2,3,4'")
    changes_made |= add_column_if_not_exists(cursor, "ticket", "related_project_id", "INTEGER", "NULL")
    
    # Incoming email account table - missing columns
    print("\n📋 Checking 'incoming_email_account' table (if exists)...")
    try:
        # First, create the table if it doesn't exist
        incoming_email_table_sql = """
        CREATE TABLE IF NOT EXISTS incoming_email_account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            name VARCHAR DEFAULT 'Support Email',
            email_address VARCHAR NOT NULL,
            project_id INTEGER,
            imap_host VARCHAR NOT NULL,
            imap_port INTEGER DEFAULT 993,
            imap_username VARCHAR NOT NULL,
            imap_password VARCHAR NOT NULL,
            imap_use_ssl BOOLEAN DEFAULT 1,
            is_active BOOLEAN DEFAULT 1,
            auto_assign_to_user_id INTEGER,
            default_priority VARCHAR DEFAULT 'medium',
            default_category VARCHAR DEFAULT 'support',
            last_checked_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (workspace_id) REFERENCES workspace(id),
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (auto_assign_to_user_id) REFERENCES user(id)
        )
        """
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incoming_email_account'")
        if cursor.fetchone():
            print("⏭️  Table 'incoming_email_account' already exists")
            changes_made |= add_column_if_not_exists(cursor, "incoming_email_account", "project_id", "INTEGER", "NULL")
        else:
            cursor.execute(incoming_email_table_sql)
            print("✅ Created table 'incoming_email_account'")
            changes_made = True
    except Exception as e:
        print(f"⚠️  Could not check/create incoming_email_account table: {e}")
    
    # ProcessedMail table - for tracking processed emails
    print("\n📋 Checking 'processedmail' table...")
    try:
        processedmail_table_sql = """
        CREATE TABLE IF NOT EXISTS processedmail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            message_id VARCHAR NOT NULL,
            email_from VARCHAR,
            subject VARCHAR,
            ticket_id INTEGER,
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (workspace_id) REFERENCES workspace(id),
            FOREIGN KEY (ticket_id) REFERENCES ticket(id)
        )
        """
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processedmail'")
        if cursor.fetchone():
            print("⏭️  Table 'processedmail' already exists")
        else:
            cursor.execute(processedmail_table_sql)
            print("✅ Created table 'processedmail'")
            # Create index for message_id lookups
            cursor.execute("CREATE INDEX IF NOT EXISTS ix_processedmail_message_id ON processedmail(message_id)")
            changes_made = True
    except Exception as e:
        print(f"⚠️  Could not check/create processedmail table: {e}")
    
    if changes_made:
        conn.commit()
        print("\n" + "=" * 60)
        print("✅ Database updated successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ℹ️  No changes needed - all columns exist")
        print("=" * 60)
    
    conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
