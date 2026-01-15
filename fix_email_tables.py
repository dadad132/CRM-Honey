"""
Fix processedmail table and ensure email-to-ticket tracking works correctly.
Run this script on the server to fix email tracking issues.
"""
import sqlite3
from datetime import datetime
import os

def fix_email_tables():
    """Ensure processedmail and other email-related tables exist"""
    db_path = os.path.join(os.path.dirname(__file__), 'data.db')
    
    # Check if running from different directory
    if not os.path.exists(db_path):
        db_path = 'data.db'
    
    if not os.path.exists(db_path):
        print("❌ Error: data.db not found!")
        print("Please run this script from the application directory.")
        return False
    
    print(f"📁 Using database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check existing tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [t[0] for t in cursor.fetchall()]
    print(f"\n📋 Existing tables: {len(existing_tables)}")
    
    # 1. Create processedmail table if it doesn't exist
    print("\n[1] Checking processedmail table...")
    if 'processedmail' not in existing_tables:
        print("   ⚠️ Table missing! Creating...")
        cursor.execute("""
            CREATE TABLE processedmail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id VARCHAR NOT NULL,
                email_from VARCHAR NOT NULL,
                subject VARCHAR NOT NULL,
                processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticket_id INTEGER REFERENCES ticket(id),
                workspace_id INTEGER NOT NULL REFERENCES workspace(id)
            )
        """)
        cursor.execute("CREATE INDEX idx_processedmail_message_id ON processedmail(message_id)")
        cursor.execute("CREATE INDEX idx_processedmail_workspace_id ON processedmail(workspace_id)")
        print("   ✅ Created processedmail table with indexes")
    else:
        print("   ✅ Table exists")
    
    # 2. Check incoming_email_account table (note: table name uses underscores)
    print("\n[2] Checking incoming_email_account table...")
    if 'incoming_email_account' not in existing_tables:
        print("   ⚠️ Table missing! Creating...")
        cursor.execute("""
            CREATE TABLE incoming_email_account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR NOT NULL,
                email_address VARCHAR NOT NULL,
                imap_host VARCHAR,
                imap_port INTEGER DEFAULT 993,
                imap_username VARCHAR,
                imap_password VARCHAR,
                imap_use_ssl BOOLEAN DEFAULT 1,
                protocol VARCHAR DEFAULT 'imap',
                is_active BOOLEAN DEFAULT 1,
                workspace_id INTEGER NOT NULL REFERENCES workspace(id),
                project_id INTEGER REFERENCES project(id),
                default_priority VARCHAR DEFAULT 'medium',
                default_category VARCHAR DEFAULT 'support',
                auto_assign_to_user_id INTEGER REFERENCES user(id),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_checked_at DATETIME
            )
        """)
        print("   ✅ Created incoming_email_account table")
    else:
        print("   ✅ Table exists")
    
    # 3. Check emailsettings table
    print("\n[3] Checking emailsettings table...")
    if 'emailsettings' not in existing_tables:
        print("   ⚠️ Table missing! Creating...")
        cursor.execute("""
            CREATE TABLE emailsettings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id INTEGER UNIQUE NOT NULL REFERENCES workspace(id),
                mail_host VARCHAR,
                mail_port INTEGER DEFAULT 587,
                mail_username VARCHAR,
                mail_password VARCHAR,
                mail_from_email VARCHAR,
                mail_from_name VARCHAR,
                mail_use_tls BOOLEAN DEFAULT 1,
                incoming_mail_host VARCHAR,
                incoming_mail_port INTEGER DEFAULT 993,
                incoming_mail_username VARCHAR,
                incoming_mail_password VARCHAR,
                incoming_mail_use_ssl BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Created emailsettings table")
    else:
        print("   ✅ Table exists")
    
    conn.commit()
    
    # 4. Show email configuration status
    print("\n" + "="*60)
    print("📧 EMAIL CONFIGURATION STATUS")
    print("="*60)
    
    # Check legacy email settings
    cursor.execute("SELECT workspace_id, incoming_mail_host, incoming_mail_username FROM emailsettings WHERE incoming_mail_host IS NOT NULL")
    legacy_settings = cursor.fetchall()
    if legacy_settings:
        print(f"\nLegacy email settings (emailsettings table):")
        for ws_id, host, username in legacy_settings:
            print(f"  • Workspace {ws_id}: {username}@{host}")
    else:
        print("\n⚠️ No legacy email settings configured")
    
    # Check new multi-account settings
    cursor.execute("SELECT workspace_id, name, email_address, imap_host, is_active, last_checked_at FROM incoming_email_account")
    accounts = cursor.fetchall()
    if accounts:
        print(f"\nIncoming email accounts (incomingemailaccount table):")
        for ws_id, name, email, host, active, last_checked in accounts:
            status = "✅ Active" if active else "❌ Inactive"
            checked = f"Last check: {last_checked}" if last_checked else "Never checked"
            print(f"  • [{status}] {name}: {email} @ {host} ({checked})")
    else:
        print("\n⚠️ No incoming email accounts configured")
    
    # 5. Show recent processed emails
    print("\n" + "="*60)
    print("📬 RECENT PROCESSED EMAILS")
    print("="*60)
    
    cursor.execute("""
        SELECT p.id, p.email_from, p.subject, p.processed_at, p.ticket_id
        FROM processedmail p
        ORDER BY p.processed_at DESC
        LIMIT 10
    """)
    processed = cursor.fetchall()
    if processed:
        for pid, email_from, subject, proc_at, ticket_id in processed:
            print(f"  [{proc_at}] From: {email_from}")
            print(f"              Subject: {subject[:50]}...")
            print(f"              Ticket ID: {ticket_id}")
            print()
    else:
        print("  No processed emails found (this could mean:")
        print("  - Email processing hasn't run yet")
        print("  - No new emails in the mailbox")
        print("  - Email settings are not configured)")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Fix complete! Restart the server to apply changes.")
    print("="*60)
    
    return True

if __name__ == "__main__":
    fix_email_tables()
