#!/usr/bin/env python3
"""
Create the incoming_email_account table for email-to-ticket processing.
Run this script on the server to fix the missing table.
"""

import sqlite3
from pathlib import Path

def create_incoming_email_account_table():
    """Create the incoming_email_account table if it doesn't exist"""
    
    db_path = Path("data.db")
    if not db_path.exists():
        print("❌ data.db not found")
        return False
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incoming_email_account'")
    if cursor.fetchone():
        print("✓ Table 'incoming_email_account' already exists")
        conn.close()
        return True
    
    print("📝 Creating 'incoming_email_account' table...")
    
    cursor.execute("""
        CREATE TABLE incoming_email_account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            name TEXT DEFAULT 'Support Email',
            email_address TEXT NOT NULL,
            project_id INTEGER,
            protocol TEXT DEFAULT 'imap',
            imap_host TEXT NOT NULL,
            imap_port INTEGER DEFAULT 993,
            imap_username TEXT NOT NULL,
            imap_password TEXT NOT NULL,
            imap_use_ssl INTEGER DEFAULT 1,
            is_active INTEGER DEFAULT 1,
            auto_assign_to_user_id INTEGER,
            default_priority TEXT DEFAULT 'medium',
            default_category TEXT DEFAULT 'support',
            last_checked_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (workspace_id) REFERENCES workspace(id),
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (auto_assign_to_user_id) REFERENCES user(id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX ix_incoming_email_account_workspace_id ON incoming_email_account(workspace_id)")
    cursor.execute("CREATE INDEX ix_incoming_email_account_project_id ON incoming_email_account(project_id)")
    cursor.execute("CREATE INDEX ix_incoming_email_account_is_active ON incoming_email_account(is_active)")
    
    conn.commit()
    print("✅ Table 'incoming_email_account' created successfully!")
    
    # Also check/create processedmail table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processedmail'")
    if not cursor.fetchone():
        print("\n📝 Creating 'processedmail' table...")
        cursor.execute("""
            CREATE TABLE processedmail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL UNIQUE,
                email_from TEXT,
                subject TEXT,
                ticket_id INTEGER,
                workspace_id INTEGER,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES ticket(id),
                FOREIGN KEY (workspace_id) REFERENCES workspace(id)
            )
        """)
        cursor.execute("CREATE INDEX ix_processedmail_message_id ON processedmail(message_id)")
        cursor.execute("CREATE INDEX ix_processedmail_workspace_id ON processedmail(workspace_id)")
        conn.commit()
        print("✅ Table 'processedmail' created successfully!")
    else:
        print("✓ Table 'processedmail' already exists")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("NEXT STEPS:")
    print("=" * 50)
    print("""
1. Go to the website: Admin → Email Accounts
2. Add a new incoming email account:
   - Name: e.g. "Support Email"
   - Email Address: e.g. "support@company.com"
   - IMAP Host: e.g. "imap.gmail.com" or "mail.server.com"
   - IMAP Port: 993 (for SSL) or 143 (no SSL)
   - Username: your email username
   - Password: your email password (use App Password for Gmail)
   - Enable SSL: Yes (recommended)

3. After adding, restart the service:
   sudo systemctl restart crm-backend
   
4. Check logs:
   sudo journalctl -u crm-backend -f | grep -i email
""")
    
    return True


if __name__ == "__main__":
    create_incoming_email_account_table()
