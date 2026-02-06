#!/usr/bin/env python3
"""Check the email-to-ticket system status"""
import sqlite3
from pathlib import Path

db_path = Path("data.db")
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

print("=" * 60)
print("Email-to-Ticket System Status Check")
print("=" * 60)

# Check if incoming_email_account table exists
print("\n1. Checking incoming_email_account table...")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incoming_email_account'")
if cur.fetchone():
    print("   ✅ Table exists")
    
    # Check for accounts
    cur.execute("SELECT id, name, email_address, is_active, project_id, last_checked_at FROM incoming_email_account")
    accounts = cur.fetchall()
    if accounts:
        print(f"   📧 Found {len(accounts)} email account(s):")
        for acc in accounts:
            print(f"      - ID {acc[0]}: {acc[1]} ({acc[2]}) - Active: {acc[3]}, Project: {acc[4]}, Last checked: {acc[5]}")
    else:
        print("   ⚠️  No email accounts configured!")
else:
    print("   ❌ Table does NOT exist - needs to be created")

# Check legacy email settings
print("\n2. Checking legacy EmailSettings table...")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emailsettings'")
if cur.fetchone():
    print("   ✅ Table exists")
    try:
        cur.execute("SELECT workspace_id, incoming_mail_host FROM emailsettings WHERE incoming_mail_host IS NOT NULL")
        settings = cur.fetchall()
        if settings:
            print(f"   📧 Found {len(settings)} workspace(s) with legacy email settings:")
            for s in settings:
                print(f"      - Workspace {s[0]}: @ {s[1]}")
        else:
            print("   ⚠️  No legacy email settings configured")
    except Exception as e:
        print(f"   ⚠️  Could not query: {e}")
else:
    print("   ❌ EmailSettings table does NOT exist")

# Check processed_mail table
print("\n3. Checking processed_mail table...")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processedmail'")
if cur.fetchone():
    print("   ✅ Table exists")
    cur.execute("SELECT COUNT(*) FROM processedmail")
    count = cur.fetchone()[0]
    print(f"   📊 {count} processed emails recorded")
    
    # Show recent entries
    cur.execute("SELECT message_id, workspace_id, processed_at FROM processedmail ORDER BY processed_at DESC LIMIT 5")
    recent = cur.fetchall()
    if recent:
        print("   📋 Recent processed emails:")
        for r in recent:
            print(f"      - {r[0][:50]}... (WS: {r[1]}, {r[2]})")
else:
    print("   ❌ ProcessedMail table does NOT exist")

# Check recent tickets from email
print("\n4. Checking recent email-created tickets...")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ticket'")
if cur.fetchone():
    # Check for tickets that look like they came from email (guest tickets or with guest_email)
    cur.execute("""
        SELECT id, ticket_number, subject, is_guest, guest_email, created_at 
        FROM ticket 
        WHERE is_guest = 1 OR guest_email IS NOT NULL
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    tickets = cur.fetchall()
    if tickets:
        print(f"   📋 Found {len(tickets)} email/guest tickets (recent):")
        for t in tickets:
            print(f"      - {t[1]}: {t[2][:40]}... (Guest: {t[3]}, Email: {t[4]}, Created: {t[5]})")
    else:
        print("   ⚠️  No email-created tickets found")

conn.close()

print("\n" + "=" * 60)
print("Diagnosis:")
print("=" * 60)
print("""
If no tickets are being created from emails, check:
1. Is the email account table created? (run migration)
2. Are there active email accounts configured?
3. Is the scheduler running? (check server logs)
4. Are the IMAP credentials correct? (test connection)
5. Are emails being marked as processed? (check processedmail)
""")
