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
    
    def __init__(self, check_interval: int = 120):
        """
        Initialize scheduler
        
        Args:
            check_interval: Seconds between checks (default: 2 minutes)
        """
        self.check_interval = check_interval
        self.running = False
        self.task = None
        self._wake_event = asyncio.Event()
        self._lock = asyncio.Lock()
    
    async def check_now(self):
        """Wake the scheduler to run an immediate email check.
        Returns after the check completes."""
        if not self.running:
            return
        # Signal the sleeping loop to wake up
        self._wake_event.set()
        # Wait briefly for the lock to be acquired (meaning a check started)
        # then wait for the lock to be released (meaning the check finished)
        for _ in range(300):  # max 30 seconds
            if self._lock.locked():
                break
            await asyncio.sleep(0.1)
        # Now wait for the check to finish
        async with self._lock:
            pass
    
    async def check_emails_task(self):
        """Background task to check emails periodically"""
        
        print(f"[Email-to-Ticket] ✅ Scheduler started (checking every {self.check_interval}s)")
        check_count = 0
        
        while self.running:
            check_count += 1
            try:
                async with self._lock:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] [Email-to-Ticket] 📧 Check #{check_count} starting...")
                    
                    total_tickets_created = 0
                    
                    # Process legacy workspace email settings (single account)
                    workspace_ids = []
                    
                    try:
                        async with AsyncSession(engine) as db:
                            # Get all workspaces with legacy email settings
                            result = await db.execute(
                                select(EmailSettings.workspace_id).where(EmailSettings.incoming_mail_host.isnot(None))
                            )
                            workspace_ids = [row[0] for row in result.all()]
                        
                        print(f"[Email-to-Ticket] Found {len(workspace_ids)} workspaces with legacy email settings")
                        
                        # Process legacy workspaces sequentially
                        for ws_id in workspace_ids:
                            await self._process_workspace(ws_id)
                    except Exception as e:
                        if "no such table" in str(e).lower():
                            print(f"[Email-to-Ticket] EmailSettings table not found - skipping legacy email check")
                        else:
                            print(f"[Email-to-Ticket] Error checking legacy email settings: {e}")
                    
                    # Process new multi-account email settings
                    await self._process_email_accounts()
                    
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] [Email-to-Ticket] ✅ Check #{check_count} complete. Next check in {self.check_interval}s")
                
                # Wait for next check OR be woken up by check_now()
                self._wake_event.clear()
                try:
                    await asyncio.wait_for(self._wake_event.wait(), timeout=self.check_interval)
                    print("[Email-to-Ticket] 🔔 Manual check requested - running immediately")
                except asyncio.TimeoutError:
                    pass  # Normal timeout, proceed with next scheduled check
                
            except asyncio.CancelledError:
                print("[Email-to-Ticket] Task cancelled")
                raise
            except Exception as e:
                print(f"[Email-to-Ticket] Error in background task: {e}")
                print(f"[Email-to-Ticket] Traceback: {traceback.format_exc()}")
                # Wait before retrying (single sleep, not double)
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
            # Load accounts in one session, then close it
            # This avoids expire_on_commit issues when processing multiple accounts
            async with AsyncSession(engine) as db:
                result = await db.execute(
                    select(IncomingEmailAccount).where(
                        IncomingEmailAccount.is_active == True
                    )
                )
                accounts = result.scalars().all()
            
            if not accounts:
                return
            
            print(f"[Email-to-Ticket] Found {len(accounts)} active incoming email account(s)")
            
            # Process each account with its own fresh session
            # Previously, all accounts shared one session and db.commit() after the
            # first account expired all remaining account objects (expire_on_commit=True),
            # causing MissingGreenlet errors on subsequent accounts
            for account in accounts:
                try:
                    async with AsyncSession(engine) as account_db:
                        tickets = await process_email_account(account_db, account)
                        if tickets:
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"[{timestamp}] Email '{account.name}': Created {len(tickets)} ticket(s) from emails")
                        
                        # Update last_checked_at
                        account.last_checked_at = datetime.utcnow()
                        account_db.add(account)
                        await account_db.commit()
                except Exception as e:
                    print(f"[Email-to-Ticket] Error processing email account '{account.name}': {e}")
                    print(f"[Email-to-Ticket] Traceback: {traceback.format_exc()}")
                    from app.core.system_logger import log_fire_and_forget
                    log_fire_and_forget('ERROR', 'Scheduler', f'Error processing account: {account.name}', str(e)[:200])
        
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


async def check_emails_now():
    """Trigger an immediate email check (wakes the scheduler)"""
    await email_scheduler.check_now()
