"""
Due Date Reminders - Background service to send email reminders for upcoming task/ticket due dates
"""
import asyncio
import logging
from datetime import datetime, date, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.email import send_email
from app.models.task import Task
from app.models.ticket import Ticket
from app.models.user import User
from app.models.assignment import Assignment
from app.models.workspace import Workspace
from app.models.notification import Notification
from app.models.enums import TaskStatus

logger = logging.getLogger(__name__)


async def send_task_reminder(
    db: AsyncSession,
    task: Task,
    user: User,
    days_until_due: int,
    workspace: Optional[Workspace] = None
):
    """Send a reminder notification and email for a task"""
    try:
        # Create in-app notification
        if days_until_due == 0:
            message = f"Task '{task.title}' is due today!"
        elif days_until_due == 1:
            message = f"Task '{task.title}' is due tomorrow"
        else:
            message = f"Task '{task.title}' is due in {days_until_due} days"
        
        notification = Notification(
            user_id=user.id,
            type='reminder',
            message=message,
            url=f'/web/tasks/{task.id}',
            related_id=task.id
        )
        db.add(notification)
        
        # Send email if user has email
        if user.email:
            site_title = workspace.site_title if workspace else 'CRM'
            subject = f"[{site_title}] Reminder: {task.title}"
            
            body = f"""
Hello {user.full_name or user.username},

This is a reminder that your task is coming up:

Task: {task.title}
{f'Description: {task.description}' if task.description else ''}
Due Date: {task.due_date.strftime('%d %B %Y') if task.due_date else 'Not set'}
Priority: {task.priority.title()}

{f"⚠️ This task is due TODAY!" if days_until_due == 0 else f"📅 Due in {days_until_due} day(s)"}

View task: /web/tasks/{task.id}

---
This is an automated reminder from {site_title}.
            """.strip()
            
            try:
                await send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )
                logger.info(f"Sent task reminder email to {user.email} for task {task.id}")
            except Exception as e:
                logger.error(f"Failed to send task reminder email: {e}")
        
        await db.commit()
        
    except Exception as e:
        logger.error(f"Error sending task reminder: {e}")
        await db.rollback()


async def send_ticket_reminder(
    db: AsyncSession,
    ticket: Ticket,
    user: User,
    days_until_due: int,
    workspace: Optional[Workspace] = None
):
    """Send a reminder notification and email for a ticket"""
    try:
        # Create in-app notification
        if days_until_due == 0:
            message = f"Ticket '{ticket.subject}' ({ticket.ticket_number}) is due today!"
        elif days_until_due == 1:
            message = f"Ticket '{ticket.subject}' ({ticket.ticket_number}) is due tomorrow"
        else:
            message = f"Ticket '{ticket.subject}' ({ticket.ticket_number}) is due in {days_until_due} days"
        
        notification = Notification(
            user_id=user.id,
            type='reminder',
            message=message,
            url=f'/web/tickets/{ticket.id}',
            related_id=ticket.id
        )
        db.add(notification)
        
        # Send email if user has email
        if user.email:
            site_title = workspace.site_title if workspace else 'CRM'
            subject = f"[{site_title}] Reminder: {ticket.ticket_number} - {ticket.subject}"
            
            scheduled_str = ticket.scheduled_date.strftime('%d %B %Y') if ticket.scheduled_date else 'Not set'
            
            body = f"""
Hello {user.full_name or user.username},

This is a reminder that a ticket requires your attention:

Ticket: {ticket.ticket_number}
Subject: {ticket.subject}
Priority: {ticket.priority.title()}
Status: {ticket.status.replace('_', ' ').title()}
Scheduled Date: {scheduled_str}

{f"⚠️ This ticket is scheduled for TODAY!" if days_until_due == 0 else f"📅 Scheduled in {days_until_due} day(s)"}

View ticket: /web/tickets/{ticket.id}

---
This is an automated reminder from {site_title}.
            """.strip()
            
            try:
                await send_email(
                    to_email=user.email,
                    subject=subject,
                    body=body
                )
                logger.info(f"Sent ticket reminder email to {user.email} for ticket {ticket.id}")
            except Exception as e:
                logger.error(f"Failed to send ticket reminder email: {e}")
        
        await db.commit()
        
    except Exception as e:
        logger.error(f"Error sending ticket reminder: {e}")
        await db.rollback()


async def process_due_date_reminders():
    """Main function to process all due date reminders"""
    logger.info("Starting due date reminder processing...")
    
    async for db in get_session():
        try:
            today = date.today()
            
            # Reminder days: today (0), tomorrow (1), and 3 days before
            reminder_days = [0, 1, 3]
            
            for days_ahead in reminder_days:
                target_date = today + timedelta(days=days_ahead)
                
                # Find tasks due on target date
                tasks_result = await db.execute(
                    select(Task, Assignment.user_id)
                    .join(Assignment, Task.id == Assignment.task_id)
                    .where(
                        Task.due_date == target_date,
                        Task.status != TaskStatus.done,
                        Task.is_archived == False
                    )
                )
                
                tasks_with_assignees = tasks_result.fetchall()
                
                for task, user_id in tasks_with_assignees:
                    # Get user
                    user = (await db.execute(
                        select(User).where(User.id == user_id)
                    )).scalar_one_or_none()
                    
                    if user and user.is_active:
                        # Get workspace for branding
                        workspace = (await db.execute(
                            select(Workspace).where(Workspace.id == user.workspace_id)
                        )).scalar_one_or_none()
                        
                        # Check if reminder already sent today for this task/user
                        existing = (await db.execute(
                            select(Notification)
                            .where(
                                Notification.user_id == user_id,
                                Notification.related_id == task.id,
                                Notification.type == 'reminder',
                                Notification.created_at >= datetime.combine(today, datetime.min.time())
                            )
                        )).scalar_one_or_none()
                        
                        if not existing:
                            await send_task_reminder(db, task, user, days_ahead, workspace)
                
                # Find tickets with scheduled_date on target date
                tickets_result = await db.execute(
                    select(Ticket)
                    .where(
                        Ticket.scheduled_date.isnot(None),
                        Ticket.status.in_(['open', 'in_progress', 'waiting']),
                        Ticket.is_archived == False
                    )
                )
                
                tickets = tickets_result.scalars().all()
                
                for ticket in tickets:
                    if ticket.scheduled_date and ticket.scheduled_date.date() == target_date:
                        # Get assigned user
                        if ticket.assigned_to_id:
                            user = (await db.execute(
                                select(User).where(User.id == ticket.assigned_to_id)
                            )).scalar_one_or_none()
                            
                            if user and user.is_active:
                                workspace = (await db.execute(
                                    select(Workspace).where(Workspace.id == user.workspace_id)
                                )).scalar_one_or_none()
                                
                                # Check if reminder already sent today
                                existing = (await db.execute(
                                    select(Notification)
                                    .where(
                                        Notification.user_id == user.id,
                                        Notification.related_id == ticket.id,
                                        Notification.type == 'reminder',
                                        Notification.created_at >= datetime.combine(today, datetime.min.time())
                                    )
                                )).scalar_one_or_none()
                                
                                if not existing:
                                    await send_ticket_reminder(db, ticket, user, days_ahead, workspace)
            
            logger.info("Due date reminder processing completed")
            
        except Exception as e:
            logger.error(f"Error in due date reminder processing: {e}")
            import traceback
            traceback.print_exc()
        
        break  # Exit the generator after one iteration


async def start_reminder_scheduler():
    """Start the reminder scheduler that runs daily"""
    logger.info("Starting due date reminder scheduler...")
    
    while True:
        try:
            # Run reminders
            await process_due_date_reminders()
            
            # Wait until next day at 8 AM
            now = datetime.now()
            tomorrow_8am = datetime.combine(
                now.date() + timedelta(days=1),
                datetime.strptime('08:00', '%H:%M').time()
            )
            
            # If it's before 8 AM today, run today at 8 AM
            today_8am = datetime.combine(
                now.date(),
                datetime.strptime('08:00', '%H:%M').time()
            )
            
            if now < today_8am:
                next_run = today_8am
            else:
                next_run = tomorrow_8am
            
            wait_seconds = (next_run - now).total_seconds()
            logger.info(f"Next reminder run at {next_run}, waiting {wait_seconds/3600:.1f} hours")
            
            await asyncio.sleep(wait_seconds)
            
        except asyncio.CancelledError:
            logger.info("Reminder scheduler stopped")
            break
        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}")
            # On error, wait 1 hour before retrying
            await asyncio.sleep(3600)
