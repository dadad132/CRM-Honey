#!/usr/bin/env python3
"""
Add performance indexes to database tables.
Run this script to improve query performance.
"""

import sqlite3
from pathlib import Path

def add_performance_indexes():
    """Add indexes to commonly queried columns"""
    
    db_path = Path("data.db")
    if not db_path.exists():
        print("❌ data.db not found")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # List of indexes to create: (index_name, table, columns)
    indexes = [
        # User lookups
        ("ix_user_workspace_id", "user", "workspace_id"),
        ("ix_user_email", "user", "email"),
        ("ix_user_is_active", "user", "is_active"),
        
        # Task queries (most common)
        ("ix_task_project_id", "task", "project_id"),
        ("ix_task_workspace_id", "task", "workspace_id"),
        ("ix_task_status", "task", "status"),
        ("ix_task_assigned_to", "task", "assigned_to"),
        ("ix_task_is_archived", "task", "is_archived"),
        ("ix_task_due_date", "task", "due_date"),
        ("ix_task_created_at", "task", "created_at"),
        
        # Project queries
        ("ix_project_workspace_id", "project", "workspace_id"),
        ("ix_project_is_archived", "project", "is_archived"),
        
        # Ticket queries
        ("ix_ticket_workspace_id", "ticket", "workspace_id"),
        ("ix_ticket_project_id", "ticket", "project_id"),
        ("ix_ticket_status", "ticket", "status"),
        ("ix_ticket_assigned_to", "ticket", "assigned_to"),
        ("ix_ticket_created_at", "ticket", "created_at"),
        ("ix_ticket_guest_email", "ticket", "guest_email"),
        
        # Notification queries
        ("ix_notification_user_id", "notification", "user_id"),
        ("ix_notification_is_read", "notification", "is_read"),
        ("ix_notification_created_at", "notification", "created_at"),
        
        # Comment queries
        ("ix_comment_task_id", "comment", "task_id"),
        ("ix_comment_user_id", "comment", "user_id"),
        
        # Ticket comment queries
        ("ix_ticketcomment_ticket_id", "ticketcomment", "ticket_id"),
        
        # Assignment queries
        ("ix_assignment_task_id", "assignment", "task_id"),
        ("ix_assignment_user_id", "assignment", "user_id"),
        
        # Meeting queries
        ("ix_meeting_workspace_id", "meeting", "workspace_id"),
        ("ix_meeting_start_time", "meeting", "start_time"),
        ("ix_meeting_is_cancelled", "meeting", "is_cancelled"),
        
        # Activity queries
        ("ix_activity_workspace_id", "activity", "workspace_id"),
        ("ix_activity_created_at", "activity", "created_at"),
        
        # Email processing
        ("ix_processedmail_message_id", "processedmail", "message_id"),
        ("ix_processedmail_workspace_id", "processedmail", "workspace_id"),
        
        # Chat queries
        ("ix_message_chat_id", "message", "chat_id"),
        ("ix_message_created_at", "message", "created_at"),
        ("ix_chatmember_chat_id", "chatmember", "chat_id"),
        ("ix_chatmember_user_id", "chatmember", "user_id"),
        
        # Lead/Deal/Contact (CRM)
        ("ix_lead_workspace_id", "lead", "workspace_id"),
        ("ix_deal_workspace_id", "deal", "workspace_id"),
        ("ix_contact_workspace_id", "contact", "workspace_id"),
        ("ix_company_workspace_id", "company", "workspace_id"),
    ]
    
    created_count = 0
    skipped_count = 0
    
    print("🔧 Adding performance indexes...")
    print("-" * 50)
    
    for index_name, table, columns in indexes:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({columns})")
            # Check if index was created
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='index' AND name='{index_name}'")
            if cursor.fetchone():
                created_count += 1
        except sqlite3.OperationalError as e:
            if "no such table" in str(e).lower():
                skipped_count += 1
            else:
                print(f"⚠️  {index_name}: {e}")
    
    # Add composite indexes for common query patterns
    composite_indexes = [
        ("ix_task_workspace_status", "task", "workspace_id, status"),
        ("ix_task_project_status", "task", "project_id, status"),
        ("ix_ticket_workspace_status", "ticket", "workspace_id, status"),
        ("ix_notification_user_read", "notification", "user_id, is_read"),
    ]
    
    for index_name, table, columns in composite_indexes:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({columns})")
            created_count += 1
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                print(f"⚠️  {index_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Created/verified {created_count} indexes")
    if skipped_count:
        print(f"ℹ️  Skipped {skipped_count} indexes (tables don't exist)")
    print("\n🚀 Database optimized for better performance!")


if __name__ == "__main__":
    add_performance_indexes()
