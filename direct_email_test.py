#!/usr/bin/env python3
"""
Direct Email Test Script
Run this directly on the server to test email-to-ticket processing
This bypasses the web framework to isolate the issue

Usage: python direct_email_test.py
"""
import sqlite3
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import socket

# Set timeout
socket.setdefaulttimeout(30)

def main():
    print("=" * 70)
    print("DIRECT EMAIL-TO-TICKET TEST")
    print("=" * 70)
    print(f"Time: {datetime.now()}")
    print()
    
    # Connect to database
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        print("✅ Connected to database")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"   Tables found: {len(tables)}")
    
    # Find email accounts
    accounts = []
    
    # Check incoming_email_account table
    if 'incoming_email_account' in tables:
        cursor.execute("""
            SELECT id, name, email_address, imap_host, imap_port, 
                   imap_username, imap_password, imap_use_ssl, is_active, workspace_id
            FROM incoming_email_account
            WHERE is_active = 1
        """)
        accounts = cursor.fetchall()
        print(f"\n📧 Found {len(accounts)} active email account(s) in incoming_email_account")
    else:
        print("\n⚠️  incoming_email_account table not found")
    
    # Check emailsettings table (legacy)
    if 'emailsettings' in tables:
        cursor.execute("""
            SELECT workspace_id, incoming_mail_host, incoming_mail_port, 
                   incoming_mail_username, incoming_mail_password, incoming_mail_use_ssl
            FROM emailsettings
            WHERE incoming_mail_host IS NOT NULL AND incoming_mail_host != ''
        """)
        legacy = cursor.fetchall()
        if legacy:
            print(f"📧 Found {len(legacy)} legacy email setting(s) in emailsettings")
            for ws_id, host, port, user, pwd, ssl in legacy:
                accounts.append((f"legacy-{ws_id}", "Legacy Settings", user, host, port, user, pwd, ssl, 1, ws_id))
    
    if not accounts:
        print("\n❌ NO EMAIL ACCOUNTS CONFIGURED!")
        print("   Go to Admin > Email Accounts and add an incoming email account")
        conn.close()
        return
    
    # Test each account
    for account in accounts:
        acc_id, name, email_addr, host, port, username, password, use_ssl, is_active, ws_id = account
        
        print("\n" + "=" * 70)
        print(f"TESTING ACCOUNT: {name}")
        print("=" * 70)
        print(f"   Email: {email_addr}")
        print(f"   Host: {host}:{port}")
        print(f"   Username: {username}")
        print(f"   SSL: {use_ssl}")
        print(f"   Workspace ID: {ws_id}")
        
        try:
            # Step 1: Connect
            print(f"\n[1] Connecting to {host}:{port}...")
            if use_ssl:
                mail = imaplib.IMAP4_SSL(host, port or 993)
            else:
                mail = imaplib.IMAP4(host, port or 143)
            print("   ✅ Connected!")
            
            # Step 2: Login
            print(f"\n[2] Logging in as {username}...")
            mail.login(username, password)
            print("   ✅ Login successful!")
            
            # Step 3: Select INBOX
            print(f"\n[3] Selecting INBOX...")
            status, data = mail.select('INBOX')
            print(f"   ✅ INBOX selected (status: {status})")
            
            # Step 4: Count all emails
            print(f"\n[4] Counting emails...")
            status, messages = mail.search(None, 'ALL')
            all_ids = messages[0].split()
            print(f"   Total emails in inbox: {len(all_ids)}")
            
            # Step 5: Search for UNSEEN
            print(f"\n[5] Searching for UNSEEN (unread) emails...")
            status, messages = mail.search(None, 'UNSEEN')
            unread_ids = messages[0].split()
            print(f"   ✅ Found {len(unread_ids)} UNREAD email(s)")
            
            if not unread_ids:
                print("\n   ⚠️  No unread emails to process!")
                print("   Make sure the test email is marked as UNREAD in your mailbox")
                mail.close()
                mail.logout()
                continue
            
            # Step 6: Show unread emails
            print(f"\n[6] Unread email details:")
            for i, eid in enumerate(unread_ids[:5]):  # Show first 5
                try:
                    status, msg_data = mail.fetch(eid, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Decode subject
                    subject_raw = msg.get('Subject', 'No Subject')
                    decoded = decode_header(subject_raw)
                    subject = ''
                    for part, charset in decoded:
                        if isinstance(part, bytes):
                            subject += part.decode(charset or 'utf-8', errors='replace')
                        else:
                            subject += str(part)
                    
                    from_addr = msg.get('From', 'Unknown')
                    date = msg.get('Date', 'Unknown')
                    
                    print(f"\n   Email #{i+1} (ID: {eid}):")
                    print(f"      From: {from_addr[:60]}")
                    print(f"      Subject: {subject[:60]}")
                    print(f"      Date: {date}")
                except Exception as e:
                    print(f"   Error reading email {eid}: {e}")
            
            # Step 7: Ask if user wants to create tickets
            print(f"\n" + "-" * 70)
            print("READY TO CREATE TICKETS")
            print("-" * 70)
            print(f"Found {len(unread_ids)} unread email(s) that can be converted to tickets.")
            
            response = input("\nDo you want to process these emails NOW? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                print("\n[7] Processing emails and creating tickets...")
                
                # Import the actual processing function
                import sys
                import os
                sys.path.insert(0, os.getcwd())
                
                import asyncio
                from app.core.database import async_session_factory
                from app.models.ticket import Ticket
                from app.core.email_to_ticket_v2 import generate_unique_ticket_number, get_local_time
                
                async def create_tickets():
                    async with async_session_factory() as db:
                        tickets_created = 0
                        
                        for eid in unread_ids:
                            try:
                                status, msg_data = mail.fetch(eid, '(RFC822)')
                                msg = email.message_from_bytes(msg_data[0][1])
                                
                                # Get email details
                                from_header = msg.get('From', '')
                                from email.utils import parseaddr
                                sender_name, sender_email = parseaddr(from_header)
                                sender_email = sender_email.lower()
                                
                                # Decode subject
                                subject_raw = msg.get('Subject', 'No Subject')
                                decoded = decode_header(subject_raw)
                                subject = ''
                                for part, charset in decoded:
                                    if isinstance(part, bytes):
                                        subject += part.decode(charset or 'utf-8', errors='replace')
                                    else:
                                        subject += str(part)
                                
                                # Get body
                                body = ''
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        if part.get_content_type() == 'text/plain':
                                            payload = part.get_payload(decode=True)
                                            if payload:
                                                body = payload.decode(errors='replace')
                                                break
                                else:
                                    payload = msg.get_payload(decode=True)
                                    if payload:
                                        body = payload.decode(errors='replace')
                                
                                if not body:
                                    body = "(No text content)"
                                
                                # Generate ticket number
                                ticket_number = await generate_unique_ticket_number(db, ws_id)
                                
                                # Create ticket
                                ticket = Ticket(
                                    ticket_number=ticket_number,
                                    subject=subject[:200],
                                    description=body[:5000],
                                    priority='medium',
                                    status='open',
                                    category='support',
                                    workspace_id=ws_id,
                                    is_guest=True,
                                    guest_name=sender_name.split()[0] if sender_name else "Unknown",
                                    guest_surname=sender_name.split()[-1] if sender_name and len(sender_name.split()) > 1 else "",
                                    guest_email=sender_email,
                                    guest_phone="",
                                    guest_company="",
                                    guest_branch="",
                                    created_at=get_local_time(),
                                    updated_at=get_local_time()
                                )
                                
                                db.add(ticket)
                                await db.commit()
                                
                                # Mark email as read
                                mail.store(eid, '+FLAGS', '\\Seen')
                                
                                print(f"   ✅ Created ticket {ticket_number} from {sender_email}")
                                tickets_created += 1
                                
                            except Exception as e:
                                print(f"   ❌ Error processing email: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        return tickets_created
                
                tickets = asyncio.run(create_tickets())
                print(f"\n   🎉 Created {tickets} ticket(s)!")
            else:
                print("\n   Skipped ticket creation.")
            
            mail.close()
            mail.logout()
            print("\n   ✅ Disconnected from mail server")
            
        except imaplib.IMAP4.error as e:
            print(f"\n   ❌ IMAP ERROR: {e}")
            print("   Check your username/password and make sure IMAP is enabled")
        except socket.timeout:
            print(f"\n   ❌ CONNECTION TIMEOUT")
            print("   The mail server did not respond in 30 seconds")
        except Exception as e:
            print(f"\n   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    conn.close()
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
