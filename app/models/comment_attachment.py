from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class CommentAttachment(SQLModel, table=True):
    """File attachment for a comment"""
    __tablename__ = "comment_attachment"
    # TODO: FUTURE FEATURE - Attachment Labels/Categories
    # Add a 'label' or 'category' field to categorize attachments:
    # Examples: "Purchase Order", "PO", "Invoice", "Quote", "Contract", "Receipt", "Reference", "Documentation"
    # Could be:
    #   - label: Optional[str] = None  # Free-text label
    #   - category: Optional[str] = None  # Predefined categories from a list
    #   - tags: Optional[str] = None  # JSON array of multiple tags
    # UI would need a dropdown or input field when uploading attachments
    # Also consider: description field for additional context about the attachment
    
    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(foreign_key="comment.id", index=True)
    filename: str  # Original filename
    file_path: str  # Path where file is stored on disk
    file_size: int  # Size in bytes
    content_type: str  # MIME type
    uploaded_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
