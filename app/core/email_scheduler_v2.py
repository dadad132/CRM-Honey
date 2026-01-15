"""
Email-to-Ticket Scheduler V2
Uses database settings for each workspace - supports multiple email accounts
"""

import asyncio
import traceback
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.core.database import engine
from app.core.email_to_ticket_v2 import process_workspace_emails, process_email_account
from app.models.workspace import Workspace
from app.models.email_settings import EmailSettings
from app.models.incoming_email_account import IncomingEmailAccount


class EmailScheduler:
    """Background scheduler for email-to-ticket processing"""
    
    def __init__(self, check_interval: int = 300):
        """
        Initialize scheduler
        
        Args:
            check_interval: Seconds between checks (default: 5 minutes)
        """
        self.check_interval = check_interval
        self.running = False
        self.task = None
    
    async def check_emails_task(self):
        """Background task to check emails periodically"""
        
        print(f"[Email-to-Ticket] ✅ Scheduler started (checking every {self.check_interval}s)")
        print(f"[Email-to-Ticket] Scheduler will check: legacy emailsettings + incoming_email_account tables")
        
        while self.running:
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n[{timestamp}] [Email-to-Ticket] ========== CHECKING EMAILS ==========")
                
                # Process legacy workspace email settings (single account)
                workspace_ids = []
                
                try:
                    async with AsyncSession(engine) as db:
                        # Get all workspaces with legacy email settings
                        result = await db.execute(
                            select(EmailSettings.workspace_id).where(EmailSettings.incoming_mail_host.isnot(None))
                        )
                        workspace_ids = [row[0] for row in result.all()]
                    
                    print(f"[Email-to-Ticket] Legacy email settings: {len(workspace_ids)} workspace(s)")
                    
                    # Process legacy workspaces sequentially
                    for ws_id in workspace_ids:
                        print(f"[Email-to-Ticket] Processing legacy workspace {ws_id}...")
                        await self._process_workspace(ws_id)
                except Exception as e:
                    if "no such table" in str(e).lower():
                        print(f"[Email-to-Ticket] Legacy emailsettings table not found - skipping")
                    else:
                        print(f"[Email-to-Ticket] ❌ Error checking legacy email settings: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Process new multi-account email settings
                print(f"[Email-to-Ticket] Checking incoming_email_account table...")
                await self._process_email_accounts()
                
                print(f"[{timestamp}] [Email-to-Ticket] ========== CHECK COMPLETE ==========\n")
                
                # Wait for next check
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                print("[Email-to-Ticket] Task cancelled")
                raise
            except Exception as e:
                print(f"[Email-to-Ticket] Error in background task: {e}")
                print(f"[Email-to-Ticket] Traceback: {traceback.format_exc()}")
                # Wait before retrying after error
                await asyncio.sleep(self.check_interval)
    
    async def _process_workspace(self, workspace_id: int):
        """Process emails for a single workspace with its own session (legacy single-account)"""
        try:
            async with AsyncSession(engine) as db:
                tickets = await process_workspace_emails(db, workspace_id)
                
                if tickets:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Workspace {workspace_id}: Created {len(tickets)} ticket(s) from emails")
        
        except Exception as e:
            print(f"[Email-to-Ticket] Error processing workspace {workspace_id}: {e}")
    
    async def _process_email_accounts(self):
        """Process emails for all active incoming email accounts (new multi-account)"""
        try:
            async with AsyncSession(engine) as db:
                # Find all active email accounts
                result = await db.execute(
                    select(IncomingEmailAccount).where(
                        IncomingEmailAccount.is_active == True
                    )
                )
                accounts = result.scalars().all()
                
                print(f"[Email-to-Ticket] Found {len(accounts)} active incoming email account(s)")
                
                if not accounts:
                    print(f"[Email-to-Ticket] No active email accounts configured - nothing to process")
                    return
                
                for account in accounts:
                    print(f"[Email-to-Ticket] Processing account: {account.name} ({account.email_address})")
                    try:
                        tickets = await process_email_account(db, account)
                        if tickets:
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"[{timestamp}] ✅ Email '{account.name}': Created {len(tickets)} ticket(s)")
                        else:
                            print(f"[Email-to-Ticket] Account '{account.name}': No new tickets created")
                        
                        # Update last_checked_at
                        account.last_checked_at = datetime.utcnow()
                        db.add(account)
                        await db.commit()
                    except Exception as e:
                        print(f"[Email-to-Ticket] ❌ Error processing email account '{account.name}': {e}")
                        print(f"[Email-to-Ticket] Traceback: {traceback.format_exc()}")
        
        except Exception as e:
            if "no such table" in str(e).lower():
                print(f"[Email-to-Ticket] IncomingEmailAccount table not found - skipping multi-account check")
            else:
                print(f"[Email-to-Ticket] Error processing email accounts: {e}")
                print(f"[Email-to-Ticket] Traceback: {traceback.format_exc()}")
    
    async def start(self):
        """Start the scheduler"""
        if self.running:
            print("[Email-to-Ticket] Scheduler already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self.check_emails_task())
        # Add exception handler to log if task crashes
        self.task.add_done_callback(self._task_done_callback)
        print("[Email-to-Ticket] Scheduler started successfully")
    
    def _task_done_callback(self, task):
        """Handle task completion/failure"""
        try:
            exception = task.exception()
            if exception:
                print(f"[Email-to-Ticket] ❌ Background task crashed: {exception}")
                print(f"[Email-to-Ticket] Traceback: {traceback.format_exception(type(exception), exception, exception.__traceback__)}")
        except asyncio.CancelledError:
            print("[Email-to-Ticket] Task was cancelled")
        except asyncio.InvalidStateError:
            pass  # Task not done yet
    
    async def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return
        
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print("[Email-to-Ticket] Scheduler stopped")


# Global scheduler instance
from app.core.config import get_settings
settings = get_settings()
email_scheduler = EmailScheduler(check_interval=settings.email_check_interval)


async def start_email_scheduler():
    """Start the email-to-ticket scheduler"""
    try:
        await email_scheduler.start()
    except Exception as e:
        print(f"[Email-to-Ticket] Failed to start scheduler: {e}")


async def stop_email_scheduler():
    """Stop the email-to-ticket scheduler"""
    await email_scheduler.stop()
