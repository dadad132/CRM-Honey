#!/usr/bin/env python3
"""
Test email processing - manually run the email-to-ticket check
"""
import asyncio
import sys
sys.path.insert(0, '.')

async def test_email_processing():
    print("=" * 60)
    print("Testing Email-to-Ticket Processing")
    print("=" * 60)
    
    from sqlmodel.ext.asyncio.session import AsyncSession
    from sqlmodel import select
    from app.core.database import engine
    from app.models.email_settings import EmailSettings
    from app.core.email_to_ticket_v2 import process_workspace_emails
    
    # Test legacy workspace email processing
    print("\n1. Testing legacy workspace email processing...")
    
    async with AsyncSession(engine) as db:
        # Get workspaces with email settings
        result = await db.execute(
            select(EmailSettings).where(EmailSettings.incoming_mail_host.isnot(None))
        )
        settings_list = result.scalars().all()
        
        if not settings_list:
            print("   ❌ No email settings found!")
            return
        
        for settings in settings_list:
            print(f"\n   📧 Processing workspace {settings.workspace_id}:")
            print(f"      IMAP: {settings.incoming_mail_host}:{settings.incoming_mail_port}")
            print(f"      User: {settings.incoming_mail_username}")
            print(f"      SSL: {settings.incoming_mail_use_ssl}")
            
            try:
                # Try to process emails
                tickets = await process_workspace_emails(db, settings.workspace_id)
                
                if tickets:
                    print(f"      ✅ Created {len(tickets)} ticket(s)!")
                    for t in tickets:
                        print(f"         - {t.ticket_number}: {t.subject[:50]}...")
                else:
                    print("      ℹ️  No new tickets created (no new emails or all already processed)")
                    
            except Exception as e:
                print(f"      ❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_email_processing())
