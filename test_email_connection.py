"""
Email-to-Ticket Diagnostic Script
Run this on the server to test email connectivity and processing
"""
import sqlite3
import imaplib
import email
from email.header import decode_header
from datetime import datetime

def test_email_system():
    print("=" * 60)
    print("EMAIL-TO-TICKET DIAGNOSTIC")
    print("=" * 60)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # 1. Check email settings tables
    print("\n[1] CHECKING DATABASE TABLES...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    
    has_emailsettings = 'emailsettings' in tables
    has_incoming_account = 'incoming_email_account' in tables
    
    print(f"   emailsettings table: {'✅ EXISTS' if has_emailsettings else '❌ MISSING'}")
    print(f"   incoming_email_account table: {'✅ EXISTS' if has_incoming_account else '❌ MISSING'}")
    
    # 2. Check legacy email settings
    print("\n[2] LEGACY EMAIL SETTINGS (emailsettings table)...")
    if has_emailsettings:
        cursor.execute("""
            SELECT workspace_id, incoming_mail_host, incoming_mail_port, 
                   incoming_mail_username, incoming_mail_use_ssl
            FROM emailsettings 
            WHERE incoming_mail_host IS NOT NULL AND incoming_mail_host != ''
        """)
        legacy = cursor.fetchall()
        if legacy:
            for ws_id, host, port, username, use_ssl in legacy:
                print(f"   Workspace {ws_id}:")
                print(f"      Host: {host}:{port}")
                print(f"      Username: {username}")
                print(f"      SSL: {use_ssl}")
                
                # Try to connect
                print(f"   Testing connection...")
                try:
                    cursor.execute("SELECT incoming_mail_password FROM emailsettings WHERE workspace_id = ?", (ws_id,))
                    password = cursor.fetchone()[0]
                    
                    if use_ssl:
                        mail = imaplib.IMAP4_SSL(host, port or 993)
                    else:
                        mail = imaplib.IMAP4(host, port or 143)
                    
                    mail.login(username, password)
                    mail.select('INBOX')
                    
                    # Check for unread emails
                    status, messages = mail.search(None, 'UNSEEN')
                    unread_ids = messages[0].split()
                    print(f"   ✅ Connection successful!")
                    print(f"   📬 Unread emails: {len(unread_ids)}")
                    
                    if unread_ids:
                        print(f"\n   Unread email subjects:")
                        for eid in unread_ids[:5]:  # Show first 5
                            status, msg_data = mail.fetch(eid, '(RFC822)')
                            msg = email.message_from_bytes(msg_data[0][1])
                            subject = msg.get('Subject', 'No Subject')
                            # Decode subject
                            decoded = decode_header(subject)
                            subject_str = ''
                            for part, charset in decoded:
                                if isinstance(part, bytes):
                                    subject_str += part.decode(charset or 'utf-8', errors='replace')
                                else:
                                    subject_str += part
                            from_addr = msg.get('From', 'Unknown')
                            print(f"      - {subject_str[:50]} (from: {from_addr[:30]})")
                    
                    mail.close()
                    mail.logout()
                except Exception as e:
                    print(f"   ❌ Connection FAILED: {e}")
        else:
            print("   No legacy email settings configured")
    else:
        print("   Table does not exist")
    
    # 3. Check incoming email accounts
    print("\n[3] INCOMING EMAIL ACCOUNTS (incoming_email_account table)...")
    if has_incoming_account:
        cursor.execute("""
            SELECT id, name, email_address, imap_host, imap_port, 
                   imap_username, imap_password, imap_use_ssl, is_active, workspace_id
            FROM incoming_email_account
        """)
        accounts = cursor.fetchall()
        if accounts:
            for acc_id, name, email_addr, host, port, username, password, use_ssl, is_active, ws_id in accounts:
                status_icon = "✅" if is_active else "❌"
                print(f"\n   [{status_icon}] Account: {name} (ID: {acc_id})")
                print(f"      Email: {email_addr}")
                print(f"      Host: {host}:{port}")
                print(f"      Username: {username}")
                print(f"      Active: {is_active}")
                print(f"      Workspace: {ws_id}")
                
                if is_active and host:
                    print(f"   Testing connection...")
                    try:
                        if use_ssl:
                            mail = imaplib.IMAP4_SSL(host, port or 993)
                        else:
                            mail = imaplib.IMAP4(host, port or 143)
                        
                        mail.login(username, password)
                        mail.select('INBOX')
                        
                        # Check for unread emails
                        status, messages = mail.search(None, 'UNSEEN')
                        unread_ids = messages[0].split()
                        print(f"   ✅ Connection successful!")
                        print(f"   📬 Unread emails: {len(unread_ids)}")
                        
                        if unread_ids:
                            print(f"\n   Unread email subjects:")
                            for eid in unread_ids[:5]:  # Show first 5
                                status, msg_data = mail.fetch(eid, '(RFC822)')
                                msg = email.message_from_bytes(msg_data[0][1])
                                subject = msg.get('Subject', 'No Subject')
                                # Decode subject
                                decoded = decode_header(subject)
                                subject_str = ''
                                for part, charset in decoded:
                                    if isinstance(part, bytes):
                                        subject_str += part.decode(charset or 'utf-8', errors='replace')
                                    else:
                                        subject_str += part
                                from_addr = msg.get('From', 'Unknown')
                                print(f"      - {subject_str[:50]} (from: {from_addr[:30]})")
                        
                        mail.close()
                        mail.logout()
                    except Exception as e:
                        print(f"   ❌ Connection FAILED: {e}")
        else:
            print("   No incoming email accounts configured")
    else:
        print("   Table does not exist")
    
    # 4. Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not has_emailsettings and not has_incoming_account:
        print("❌ NO EMAIL TABLES FOUND!")
        print("   The email-to-ticket system is not set up.")
        print("   Configure email settings in Admin > Email Settings")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("If emails are not being processed, check:")
    print("1. Is the email scheduler running? Check logs with:")
    print("   sudo journalctl -u crm-backend --since '10 minutes ago' | grep -i email")
    print("2. Are there any errors in the logs?")
    print("3. Is the email marked as UNREAD in your mailbox?")
    print("=" * 60)

if __name__ == "__main__":
    test_email_system()
