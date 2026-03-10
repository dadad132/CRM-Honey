from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class SystemLog(SQLModel, table=True):
    """Lightweight diagnostic log for email processing and system events.
    Auto-deleted after 7 days to keep database size small."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    level: str = Field(default="INFO", max_length=10)  # INFO, WARN, ERROR, DEBUG
    category: str = Field(default="email", max_length=30, index=True)  # email, system, ticket, etc.
    source: str = Field(default="", max_length=50)  # e.g. "IMAP", "Email Account", "Scheduler"
    message: str  # Short log message
    details: Optional[str] = Field(default=None)  # Extra context (message_id, ticket#, etc.) - kept short
    workspace_id: Optional[int] = Field(default=None, index=True)
