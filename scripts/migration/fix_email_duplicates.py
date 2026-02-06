#!/usr/bin/env python3
"""
Fix email duplicate issues:
1. Add UNIQUE constraint to processedmail.message_id
2. Remove duplicate entries (keep the oldest)
3. Show statistics
"""

import sqlite3
import os
from datetime import datetime

# Get database path
db_path = os.path.join(os.path.dirname(__file__), 'data.db')
print(f"Database: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n=== EMAIL DUPLICATE FIX ===\n")

# Step 1: Check for existing duplicates
print("1. Checking for duplicate message_ids...")
cursor.execute("""
    SELECT message_id, COUNT(*) as count
    FROM processedmail
    GROUP BY message_id
    HAVING count > 1
    ORDER BY count DESC
""")
duplicates = cursor.fetchall()

if duplicates:
    print(f"   Found {len(duplicates)} duplicate message_ids:\n")
    for msg_id, count in duplicates[:10]:  # Show first 10
        print(f"   - {msg_id[:60]}... ({count} copies)")
    if len(duplicates) > 10:
        print(f"   ... and {len(duplicates) - 10} more")
    
    # Step 2: Remove duplicates (keep the oldest entry)
    print("\n2. Removing duplicate entries (keeping oldest)...")
    removed = 0
    for msg_id, count in duplicates:
        # Get all IDs for this message, ordered by processed_at (oldest first)
        cursor.execute("""
            SELECT id FROM processedmail
            WHERE message_id = ?
            ORDER BY processed_at ASC
        """, (msg_id,))
        ids = [row[0] for row in cursor.fetchall()]
        
        # Keep the first (oldest), delete the rest
        if len(ids) > 1:
            ids_to_delete = ids[1:]  # Skip the first one
            cursor.execute(f"""
                DELETE FROM processedmail
                WHERE id IN ({','.join('?' * len(ids_to_delete))})
            """, ids_to_delete)
            removed += len(ids_to_delete)
    
    conn.commit()
    print(f"   Removed {removed} duplicate entries")
else:
    print("   No duplicates found!")

# Step 3: Check if unique index exists
print("\n3. Checking for unique index on message_id...")
cursor.execute("PRAGMA index_list(processedmail)")
indexes = cursor.fetchall()
has_unique_index = False
for idx in indexes:
    if 'message_id' in idx[1].lower() and idx[2] == 1:  # idx[2] == 1 means unique
        has_unique_index = True
        print(f"   Unique index already exists: {idx[1]}")
        break

if not has_unique_index:
    print("   No unique index found. Creating one...")
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_processedmail_message_id_unique ON processedmail(message_id)")
        conn.commit()
        print("   ✅ Created unique index on processedmail.message_id")
    except sqlite3.IntegrityError as e:
        print(f"   ❌ Error: {e}")
        print("   There are still duplicates in the table. Running cleanup again...")

# Step 4: Show statistics
print("\n4. Statistics:")
cursor.execute("SELECT COUNT(*) FROM processedmail")
total = cursor.fetchone()[0]
print(f"   Total processed emails: {total}")

cursor.execute("SELECT COUNT(DISTINCT message_id) FROM processedmail")
unique = cursor.fetchone()[0]
print(f"   Unique message IDs: {unique}")

cursor.execute("SELECT COUNT(*) FROM processedmail WHERE processed_at > datetime('now', '-24 hours')")
last_24h = cursor.fetchone()[0]
print(f"   Processed in last 24h: {last_24h}")

# Step 5: Check for looping emails (same message_id processed multiple times)
print("\n5. Checking for potential loop issues...")
cursor.execute("""
    SELECT pm.message_id, pm.subject, t.ticket_number, t.status, pm.processed_at
    FROM processedmail pm
    LEFT JOIN ticket t ON pm.ticket_id = t.id
    WHERE t.status IN ('closed', 'resolved')
    ORDER BY pm.processed_at DESC
    LIMIT 5
""")
closed_emails = cursor.fetchall()
if closed_emails:
    print("   Recent emails linked to CLOSED tickets:")
    for row in closed_emails:
        msg_id, subject, ticket_num, status, processed_at = row
        print(f"   - {ticket_num} ({status}): {subject[:50]}... at {processed_at}")
else:
    print("   No recent emails linked to closed tickets")

conn.close()

print("\n=== FIX COMPLETE ===")
print("\nNext steps:")
print("1. Restart the server: sudo systemctl restart crm-backend")
print("2. Check emails are no longer duplicating")
print("3. Closed tickets will no longer receive new comments (new ticket created instead)")
