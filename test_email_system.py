#!/usr/bin/env python3
"""
Email-to-Ticket Test Script
Run this on the server to test email processing and see exactly what's happening.
"""

import asyncio
import sys
import sqlite3
from datetime import datetime, timedelta

# Add project to path
sys.path.insert(0, '.')

async def test_email_processing():
    print("=" * 70)
    print("EMAIL-TO-TICKET TEST")
    print("=" * 70)
    print(f"Time: {datetime.now()}")
    print()
    
    # Step 1: Check database for email accounts
    print("📧 STEP 1: Checking Email Accounts...")
    print("-" * 50)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, name, email_address, imap_host, imap_port, imap_use_ssl, 
                   imap_username, imap_password, is_active, workspace_id
            FROM incomingemailaccount
            WHERE is_active = 1
        """)
        accounts = cursor.fetchall()
        
        if not accounts:
            print("❌ NO ACTIVE EMAIL ACCOUNTS!")
            print("   Go to Admin → Email Accounts to add/enable one")
            conn.close()
            return
        
        print(f"Found {len(accounts)} active account(s)")
        
        for acc in accounts:
            account_id, name, email, host, port, use_ssl, username, password, is_active, workspace_id = acc
            print(f"\n  📬 Account: {name}")
            print(f"     Email: {email}")
            print(f"     IMAP: {host}:{port} (SSL: {use_ssl})")
            print(f"     Username: {username}")
            print(f"     Password: {'*' * len(password) if password else 'NOT SET!'}")
            print(f"     Workspace ID: {workspace_id}")
            
            # Step 2: Test IMAP connection
            print(f"\n  🔌 Testing IMAP connection...")
            
            import imaplib
            import socket
            
            try:
                socket.setdefaulttimeout(15)  # 15 second timeout
                
                actual_port = port or (993 if use_ssl else 143)
                
                if use_ssl:
                    mail = imaplib.IMAP4_SSL(host, actual_port)
                else:
                    mail = imaplib.IMAP4(host, actual_port)
                
                print(f"     ✅ Connected to {host}:{actual_port}")
                
                # Try to login
                mail.login(username, password)
                print(f"     ✅ Login successful")
                
                # Select inbox
                mail.select('INBOX')
                print(f"     ✅ Selected INBOX")
                
                # Search for recent emails
                date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
                status, messages = mail.search(None, f'SINCE {date_since}')
                email_ids = messages[0].split()
                print(f"     📨 Found {len(email_ids)} emails from last 7 days")
                
                # Check unread
                status, unread = mail.search(None, 'UNSEEN')
                unread_ids = unread[0].split()
                print(f"     📬 Unread emails: {len(unread_ids)}")
                
                # Show last 5 email subjects
                if email_ids:
                    print(f"\n     Last 5 emails:")
                    for email_id in email_ids[-5:]:
                        try:
                            status, msg_data = mail.fetch(email_id, '(RFC822.HEADER)')
                            if msg_data and msg_data[0]:
                                import email
                                from email.header import decode_header
                                
                                msg = email.message_from_bytes(msg_data[0][1])
                                subject = msg.get('Subject', 'No Subject')
                                from_addr = msg.get('From', 'Unknown')
                                message_id = msg.get('Message-ID', 'No ID')
                                
                                # Decode subject
                                if subject:
                                    decoded = decode_header(subject)
                                    subject = ''
                                    for part, encoding in decoded:
                                        if isinstance(part, bytes):
                                            subject += part.decode(encoding or 'utf-8', errors='ignore')
                                        else:
                                            subject += part
                                
                                # Check if already processed
                                cursor.execute("SELECT id FROM processedmail WHERE message_id = ?", (message_id,))
                                is_processed = cursor.fetchone() is not None
                                status_icon = "✓" if is_processed else "○"
                                
                                print(f"       {status_icon} From: {from_addr[:40]}")
                                print(f"         Subject: {subject[:50]}")
                                print(f"         Message-ID: {message_id[:50]}...")
                                print(f"         Processed: {'Yes' if is_processed else 'NO - will create ticket'}")
                                print()
                        except Exception as e:
                            print(f"       Error reading email: {e}")
                
                mail.close()
                mail.logout()
                
            except socket.timeout:
                print(f"     ❌ CONNECTION TIMEOUT!")
                print(f"        The server took too long to respond.")
                print(f"        Possible causes:")
                print(f"          - Firewall blocking port {actual_port}")
                print(f"          - Wrong IMAP server address")
                print(f"          - Server is down")
            except imaplib.IMAP4.error as e:
                print(f"     ❌ IMAP ERROR: {e}")
                print(f"        Possible causes:")
                print(f"          - Wrong username/password")
                print(f"          - IMAP not enabled on email account")
                print(f"          - App password required (Gmail)")
            except Exception as e:
                print(f"     ❌ CONNECTION FAILED: {e}")
        
        # Step 3: Check processed emails
        print("\n\n📋 STEP 2: Recently Processed Emails...")
        print("-" * 50)
        
        cursor.execute("""
            SELECT message_id, email_from, subject, ticket_id, processed_at
            FROM processedmail
            ORDER BY processed_at DESC
            LIMIT 10
        """)
        processed = cursor.fetchall()
        
        if processed:
            print(f"Last {len(processed)} processed emails:")
            for p in processed:
                msg_id, from_addr, subject, ticket_id, proc_time = p
                print(f"  • {from_addr}")
                print(f"    Subject: {subject[:50] if subject else 'N/A'}...")
                print(f"    Ticket ID: {ticket_id}, Processed: {proc_time}")
                print()
        else:
            print("  No processed emails found in database")
        
        # Step 4: Check recent tickets
        print("\n📋 STEP 3: Recent Tickets...")
        print("-" * 50)
        
        cursor.execute("""
            SELECT ticket_number, subject, guest_email, status, created_at
            FROM ticket
            ORDER BY created_at DESC
            LIMIT 5
        """)
        tickets = cursor.fetchall()
        
        if tickets:
            for t in tickets:
                print(f"  {t[0]}: {t[1][:40]}...")
                print(f"    From: {t[2]}, Status: {t[3]}, Created: {t[4]}")
                print()
        else:
            print("  No tickets found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("TROUBLESHOOTING TIPS")
    print("=" * 70)
    print("""
If emails are not creating tickets:

1. Check if Message-ID is already in processedmail table
   → Once processed, an email won't create another ticket
   → To reprocess: DELETE FROM processedmail WHERE message_id = '...'

2. Check IMAP connection
   → Make sure firewall allows ports 993 (SSL) or 143
   → Test: telnet mail.server.com 993

3. For Gmail:
   → Enable IMAP in Gmail settings
   → Use App Password (not regular password)
   → Enable "Less secure apps" or use OAuth

4. Manually trigger email check:
   → Go to Tickets page → Click "Check Emails" button (admin only)
   → Or: curl -X POST http://localhost:8000/web/tickets/process-emails

5. Check server logs:
   → sudo journalctl -u crm-backend -n 100 --no-pager | grep -i email
""")


if __name__ == "__main__":
    asyncio.run(test_email_processing())
