"""Check database status and email processing"""
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print("Tables in database:")
for t in tables:
    print(f"  - {t}")

# Check for processedmail table
if 'processedmail' in tables:
    print("\n\n=== PROCESSED MAIL ===")
    cursor.execute("SELECT id, message_id, subject, ticket_id, processed_at, workspace_id FROM processedmail ORDER BY processed_at DESC LIMIT 10")
    rows = cursor.fetchall()
    for r in rows:
        print(r)
else:
    print("\n⚠️ processedmail table does not exist! Email tracking may not work.")

# Check recent tickets
print("\n\n=== RECENT TICKETS ===")
cursor.execute("SELECT id, ticket_number, subject, created_at, status FROM ticket ORDER BY created_at DESC LIMIT 10")
tickets = cursor.fetchall()
for t in tickets:
    print(t)

# Check email settings
print("\n\n=== EMAIL SETTINGS ===")
if 'emailsettings' in tables:
    cursor.execute("SELECT id, workspace_id, incoming_mail_host, incoming_mail_username FROM emailsettings")
    settings = cursor.fetchall()
    for s in settings:
        print(s)
else:
    print("No emailsettings table")

# Check incoming email accounts
print("\n\n=== INCOMING EMAIL ACCOUNTS ===")
if 'incomingemailaccount' in tables:
    cursor.execute("SELECT id, name, email_address, imap_host, is_active, workspace_id, last_checked_at FROM incomingemailaccount")
    accounts = cursor.fetchall()
    for a in accounts:
        print(a)
else:
    print("No incomingemailaccount table")

# Check current time settings
print("\n\n=== TIME CHECK ===")
from datetime import datetime, timezone, timedelta
print(f"Current UTC time: {datetime.now(timezone.utc)}")
print(f"Current local time (system): {datetime.now()}")

# Check timezone in database (workspace or site settings)
if 'sitesettings' in tables:
    print("\n=== SITE SETTINGS ===")
    cursor.execute("SELECT * FROM sitesettings LIMIT 1")
    cols = [d[0] for d in cursor.description]
    row = cursor.fetchone()
    if row:
        for i, col in enumerate(cols):
            if 'time' in col.lower() or 'zone' in col.lower():
                print(f"  {col}: {row[i]}")

conn.close()
