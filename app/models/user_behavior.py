"""
User Behavior Tracking - Learns from user actions to provide smart suggestions
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBehavior(SQLModel, table=True):
    """
    Tracks user behavior patterns for learning and suggestions.
    Records actions like task creation, assignments, priorities chosen, etc.
    """
    __tablename__ = "userbehavior"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    
    # What action was taken
    action_type: str = Field(index=True)  # task_created, task_assigned, priority_set, status_changed, etc.
    
    # Context of the action
    entity_type: str  # task, ticket, project
    entity_id: Optional[int] = None
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    
    # Key-value data about the action
    field_name: Optional[str] = None  # e.g., "priority", "assignee", "status"
    field_value: Optional[str] = None  # e.g., "high", "user_5", "in_progress"
    
    # Additional context (JSON string)
    context_data: Optional[str] = None  # Store additional metadata as JSON
    
    # Time patterns
    hour_of_day: int = Field(default=0)  # 0-23, when action was taken
    day_of_week: int = Field(default=0)  # 0=Mon, 6=Sun
    
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class UserPreference(SQLModel, table=True):
    """
    Learned preferences for each user - aggregated from behavior.
    Updated periodically by analyzing UserBehavior records.
    """
    __tablename__ = "userpreference"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    
    # Preference category
    category: str = Field(index=True)  # assignee, priority, project, work_hours, task_duration
    
    # The learned value
    preference_key: str  # e.g., "default_priority", "frequent_assignee_1"
    preference_value: str  # e.g., "high", "5" (user_id)
    
    # How confident we are (0.0 - 1.0)
    confidence: float = Field(default=0.5)
    
    # How many times this pattern was observed
    occurrence_count: int = Field(default=1)
    
    # Last time this preference was observed/updated
    last_observed: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SmartSuggestion(SQLModel, table=True):
    """
    Pre-computed suggestions shown to users based on their patterns.
    """
    __tablename__ = "smartsuggestion"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    
    # What we're suggesting
    suggestion_type: str  # task_template, assignee, priority, due_date, similar_task
    
    # Context for when to show this suggestion
    context_type: Optional[str] = None  # new_task, new_ticket, project_X
    context_value: Optional[str] = None
    
    # The suggestion content (JSON)
    suggestion_data: str  # JSON with suggestion details
    
    # Ranking
    relevance_score: float = Field(default=0.5)
    
    # Tracking
    times_shown: int = Field(default=0)
    times_accepted: int = Field(default=0)
    times_dismissed: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
