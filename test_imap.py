#!/usr/bin/env python3
"""
Test IMAP connection and check inbox status
"""
import imaplib
import asyncio
import sys
sys.path.insert(0, '.')

async def test_imap():
    print("=" * 60)
    print("IMAP Connection Test")
    print("=" * 60)
    
    from sqlmodel.ext.asyncio.session import AsyncSession
    from sqlmodel import select
    from app.core.database import engine
    from app.models.email_settings import EmailSettings
    
    async with AsyncSession(engine) as db:
        result = await db.execute(
            select(EmailSettings).where(EmailSettings.incoming_mail_host.isnot(None))
        )
        settings = result.scalars().first()
        
        if not settings:
            print("❌ No email settings found!")
            return
    
    print(f"\n📧 IMAP Settings:")
    print(f"   Host: {settings.incoming_mail_host}")
    print(f"   Port: {settings.incoming_mail_port}")
    print(f"   User: {settings.incoming_mail_username}")
    print(f"   SSL: {settings.incoming_mail_use_ssl}")
    
    try:
        print("\n🔌 Connecting to IMAP server...")
        
        if settings.incoming_mail_use_ssl:
            mail = imaplib.IMAP4_SSL(settings.incoming_mail_host, settings.incoming_mail_port or 993)
        else:
            mail = imaplib.IMAP4(settings.incoming_mail_host, settings.incoming_mail_port or 143)
        
        mail.login(settings.incoming_mail_username, settings.incoming_mail_password)
        print("   ✅ Login successful!")
        
        mail.select('INBOX')
        
        # Check for ALL emails
        status, messages = mail.search(None, 'ALL')
        all_emails = messages[0].split()
        print(f"\n📊 Inbox Stats:")
        print(f"   Total emails: {len(all_emails)}")
        
        # Check for UNSEEN emails
        status, messages = mail.search(None, 'UNSEEN')
        unseen_emails = messages[0].split()
        print(f"   Unread emails: {len(unseen_emails)}")
        
        # Check for recent emails (last 7 days)
        from datetime import datetime, timedelta
        date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'SINCE {date_since}')
        recent_emails = messages[0].split()
        print(f"   Emails since {date_since}: {len(recent_emails)}")
        
        # Show subjects of recent unread emails
        if unseen_emails:
            print(f"\n📬 Unread Email Subjects:")
            for email_id in unseen_emails[:10]:
                status, msg_data = mail.fetch(email_id, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])')
                if msg_data and msg_data[0]:
                    header_data = msg_data[0][1].decode('utf-8', errors='ignore')
                    print(f"   - {header_data.strip()[:80]}...")
        else:
            print("\n⚠️  No unread emails! All emails have been marked as read.")
            print("   This explains why no tickets are being created.")
            print("\n   Possible solutions:")
            print("   1. Change the email search from UNSEEN to check all emails")
            print("   2. Use message IDs to track processed emails instead of relying on read/unread")
            print("   3. Mark emails as unread from the mail server")
        
        # Show the last few email subjects regardless of read status
        if all_emails:
            print(f"\n📧 Last 5 emails (any status):")
            for email_id in all_emails[-5:]:
                status, msg_data = mail.fetch(email_id, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)] FLAGS)')
                if msg_data and msg_data[0]:
                    header_data = msg_data[0][1].decode('utf-8', errors='ignore')
                    # Get flags
                    flags_data = msg_data[1] if len(msg_data) > 1 else b''
                    print(f"   - {header_data.strip()[:100]}... {flags_data}")
        
        mail.close()
        mail.logout()
        print("\n✅ Connection test complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_imap())
