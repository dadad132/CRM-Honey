import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

# List all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("Tables:", tables)

# Check incoming_email_account
print("\n=== incoming_email_account ===")
c.execute("SELECT id, workspace_id, name, email_address, imap_host, imap_port, imap_use_ssl FROM incoming_email_account")
for row in c.fetchall():
    print(row)

# Check emailsettings if exists
if 'emailsettings' in tables:
    print("\n=== emailsettings ===")
    c.execute("SELECT * FROM emailsettings")
    for row in c.fetchall():
        print(row)
else:
    print("\n=== No emailsettings table ===")

conn.close()
