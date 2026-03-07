from __future__ import annotations

from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel
from enum import Enum


class ActivityType(str, Enum):
    call = "call"
    email = "email"
    meeting = "meeting"
    note = "note"
    task = "task"


class Activity(SQLModel, table=True):
    """Activity log for CRM (calls, emails, meetings, notes)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_type: ActivityType
    subject: str
    description: Optional[str] = None
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id", index=True)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id", index=True)
    lead_id: Optional[int] = Field(default=None, foreign_key="lead.id", index=True)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal.id", index=True)
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
