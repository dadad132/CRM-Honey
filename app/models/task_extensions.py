from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskDependency(SQLModel, table=True):
    """Tracks task dependencies - which tasks block other tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)  # The task that is blocked
    depends_on_task_id: int = Field(foreign_key="task.id", index=True)  # The task it depends on
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TaskWatcher(SQLModel, table=True):
    """Users watching a task for updates"""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TicketWatcher(SQLModel, table=True):
    """Users watching a ticket for updates"""
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecurringTask(SQLModel, table=True):
    """Template for recurring tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    title: str
    description: Optional[str] = None
    status: str = "pending"  # Uses TaskStatus values
    priority: str = "medium"  # Uses TaskPriority values
    recurrence_type: str  # daily, weekly, monthly, yearly
    recurrence_value: Optional[str] = None  # e.g., "monday,wednesday" for weekly, "15" for monthly
    recurrence_interval: int = Field(default=1)  # Every X days/weeks/months
    start_date: datetime
    end_date: Optional[datetime] = None  # When to stop creating instances
    last_created_at: Optional[datetime] = None  # When the last instance was created
    next_due_date: Optional[datetime] = None  # When the next instance should be created
    created_by_id: int = Field(foreign_key="user.id")
    assign_to_id: Optional[int] = Field(default=None, foreign_key="user.id")  # Default assignee
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecurringTaskInstance(SQLModel, table=True):
    """Tracks created instances from recurring tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    recurring_task_id: int = Field(foreign_key="recurringtask.id", index=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    due_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaskAttachment(SQLModel, table=True):
    """File attachments on tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    filename: str
    file_path: str  # Path to stored file
    file_size: int  # Size in bytes
    file_type: Optional[str] = None  # MIME type
    uploaded_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TimeLog(SQLModel, table=True):
    """Track time spent on tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    user_id: int = Field(foreign_key="user.id")
    hours: float
    description: Optional[str] = None
    logged_at: datetime = Field(default_factory=datetime.utcnow)


class ActivityLog(SQLModel, table=True):
    """Centralized activity feed for entire workspace"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    user_id: int = Field(foreign_key="user.id")  # Who performed the action
    action_type: str  # created, updated, commented, assigned, completed, etc.
    entity_type: str  # task, project, meeting, chat, etc.
    entity_id: int  # ID of the affected entity
    details: Optional[str] = None  # JSON string with action details
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class CustomField(SQLModel, table=True):
    """Custom fields for projects/tasks"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    name: str
    field_type: str  # text, number, select, multiselect, date, checkbox, url
    options: Optional[str] = None  # JSON array for select/multiselect options
    applies_to: str  # task, project, contact, lead, deal
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CustomFieldValue(SQLModel, table=True):
    """Values for custom fields"""
    id: Optional[int] = Field(default=None, primary_key=True)
    custom_field_id: int = Field(foreign_key="customfield.id")
    entity_type: str  # task, project, contact, etc.
    entity_id: int  # ID of the task/project/etc
    value: str  # Stored as string, parsed based on field_type
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SavedView(SQLModel, table=True):
    """Save custom filter/sort configurations"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    user_id: int = Field(foreign_key="user.id")  # Owner of the view
    name: str
    view_type: str  # list, board, calendar, table, gantt
    filters: str  # JSON string of filter configuration
    sort_by: Optional[str] = None
    is_shared: bool = False  # Share with workspace or keep private
    created_at: datetime = Field(default_factory=datetime.utcnow)
