#!/usr/bin/env python3
"""
Email Diagnostic Script - Run this on the server to see why emails aren't creating tickets
"""

import asyncio
import sys
import sqlite3
from datetime import datetime

def run_diagnostic():
    print("=" * 60)
    print("EMAIL TO TICKET DIAGNOSTIC")
    print("=" * 60)
    print(f"Current time: {datetime.now()}")
    print()
    
    # Check database
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Check incoming email accounts
        print("📧 INCOMING EMAIL ACCOUNTS:")
        print("-" * 40)
        try:
            cursor.execute("""
                SELECT id, name, email_address, imap_host, imap_port, imap_use_ssl, 
                       is_active, last_checked_at, workspace_id
                FROM incomingemailaccount
            """)
            accounts = cursor.fetchall()
            
            if not accounts:
                print("❌ NO EMAIL ACCOUNTS CONFIGURED!")
                print("   Go to Admin → Email Accounts to add one")
            else:
                for acc in accounts:
                    print(f"\n  Account: {acc[1]}")
                    print(f"    Email: {acc[2]}")
                    print(f"    IMAP Host: {acc[3]}:{acc[4]} (SSL: {acc[5]})")
                    print(f"    Active: {'✅ Yes' if acc[6] else '❌ No'}")
                    print(f"    Last Check: {acc[7] or 'Never'}")
                    print(f"    Workspace ID: {acc[8]}")
                    
                    if acc[6]:  # If active, test connection
                        print(f"\n    Testing connection to {acc[3]}...")
                        test_imap_connection(acc[3], acc[4], acc[5])
        except Exception as e:
            print(f"❌ Error reading email accounts: {e}")
        
        # Check recent processed emails
        print("\n\n📬 RECENTLY PROCESSED EMAILS (last 10):")
        print("-" * 40)
        try:
            cursor.execute("""
                SELECT message_id, email_from, subject, ticket_id, processed_at
                FROM processedmail
                ORDER BY processed_at DESC
                LIMIT 10
            """)
            processed = cursor.fetchall()
            
            if not processed:
                print("  No emails have been processed yet")
            else:
                for p in processed:
                    print(f"\n  From: {p[1]}")
                    print(f"  Subject: {p[2][:50]}...")
                    print(f"  Ticket ID: {p[3]}")
                    print(f"  Processed: {p[4]}")
        except Exception as e:
            print(f"  Table doesn't exist or error: {e}")
        
        # Check recent tickets
        print("\n\n🎫 RECENT TICKETS (last 10):")
        print("-" * 40)
        try:
            cursor.execute("""
                SELECT ticket_number, subject, guest_email, status, created_at
                FROM ticket
                ORDER BY created_at DESC
                LIMIT 10
            """)
            tickets = cursor.fetchall()
            
            if not tickets:
                print("  No tickets found")
            else:
                for t in tickets:
                    print(f"\n  {t[0]}: {t[1][:40]}...")
                    print(f"    From: {t[2]}, Status: {t[3]}")
                    print(f"    Created: {t[4]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n")
    print("=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    print("""
1. If IMAP connection fails:
   - Check firewall allows outbound port 993 (SSL) or 143
   - Verify IMAP credentials are correct
   - Try telnet to test: telnet mail.server.com 993
   
2. If emails processed but no tickets:
   - Check the processedmail table - emails may already be marked processed
   - Verify workspace_id matches between account and workspace

3. To manually trigger email check:
   - Go to Tickets page and click "Check Emails" button (admin only)
   - Or run: curl http://localhost:8000/web/tickets/process-emails
   
4. Check server logs for errors:
   - sudo journalctl -u crm-backend -n 100 | grep -i email
""")


def test_imap_connection(host, port, use_ssl):
    """Test IMAP connection"""
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        actual_port = port or (993 if use_ssl else 143)
        result = sock.connect_ex((host, actual_port))
        
        if result == 0:
            print(f"    ✅ Connection to {host}:{actual_port} SUCCESSFUL")
        else:
            print(f"    ❌ Connection to {host}:{actual_port} FAILED (error code: {result})")
        
        sock.close()
    except socket.timeout:
        print(f"    ❌ Connection TIMEOUT - firewall may be blocking port {actual_port}")
    except Exception as e:
        print(f"    ❌ Connection error: {e}")


if __name__ == "__main__":
    run_diagnostic()
