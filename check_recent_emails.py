#!/usr/bin/env python3
"""Check recent email processing"""
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('data.db')
cur = conn.cursor()

print("=" * 60)
print("Recent Email Processing Check")
print("=" * 60)

# Check processed emails since Dec 15
print("\n1. Emails processed since Dec 15:")
cur.execute("SELECT message_id, processed_at, workspace_id FROM processedmail WHERE processed_at > '2025-12-15' ORDER BY processed_at DESC")
rows = cur.fetchall()
print(f"   Total: {len(rows)}")
for r in rows[:15]:
    print(f"   {r[1]}: {r[0][:50]}... (WS: {r[2]})")

# Check tickets created since Dec 15
print("\n2. Tickets created since Dec 15:")
cur.execute("SELECT ticket_number, subject, is_guest, guest_email, created_at FROM ticket WHERE created_at > '2025-12-15' ORDER BY created_at DESC")
tickets = cur.fetchall()
print(f"   Total: {len(tickets)}")
for t in tickets[:10]:
    print(f"   {t[4]}: {t[0]} - {t[1][:40]}... (Guest: {t[2]}, Email: {t[3]})")

# Check IMAP settings
print("\n3. Legacy Email Settings:")
cur.execute("SELECT workspace_id, incoming_mail_host, incoming_mail_port, incoming_mail_username FROM emailsettings")
settings = cur.fetchall()
for s in settings:
    print(f"   Workspace {s[0]}: {s[2]}@{s[1]}:{s[2]}, User: {s[3]}")

conn.close()
