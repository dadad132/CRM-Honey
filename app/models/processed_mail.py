"""
ProcessedMail Model - Tracks emails that have been converted to tickets
"""
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, UniqueConstraint


class ProcessedMail(SQLModel, table=True):
    """Track processed emails to prevent duplicate ticket creation"""
    __tablename__ = "processedmail"
    __table_args__ = (
        UniqueConstraint("message_id", "email_account", name="uq_processedmail_msg_account"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str = Field(index=True)  # Email Message-ID header
    email_from: str  # Sender email address
    subject: str  # Email subject
    processed_at: datetime = Field(default_factory=datetime.utcnow)
    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    email_account: str = Field(default="", index=True)  # Which account received this email
