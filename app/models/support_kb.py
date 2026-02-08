"""
Support Knowledge Base Models
Self-learning knowledge base for tech support chatbot
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class SupportArticle(SQLModel, table=True):
    """Knowledge base articles learned from support interactions"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    
    # Problem identification
    problem_keywords: str  # Comma-separated keywords for matching
    problem_title: str  # Short title of the problem
    problem_description: str  # Full description of the problem
    category: str = Field(default="general", index=True)  # Category like "printer", "network", "software"
    
    # Solution
    solution_steps: str  # Step-by-step solution (stored as numbered list or JSON)
    solution_source: str = Field(default="web")  # "web", "manual", "ticket"
    source_url: Optional[str] = None  # URL if sourced from web
    source_ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    
    # Learning metrics
    times_shown: int = Field(default=0)  # How many times this solution was shown
    times_helpful: int = Field(default=0)  # How many times marked as helpful
    times_not_helpful: int = Field(default=0)  # How many times marked as not helpful
    success_rate: float = Field(default=0.0)  # Calculated success rate
    
    # Management
    is_verified: bool = Field(default=False)  # Admin verified as accurate
    is_active: bool = Field(default=True)  # Still being shown to users
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SupportConversation(SQLModel, table=True):
    """Track support bot conversations for analytics"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    session_id: str = Field(index=True)  # Browser session identifier
    
    # Guest info (optional)
    guest_email: Optional[str] = Field(default=None, index=True)
    guest_name: Optional[str] = None
    
    # Conversation tracking
    initial_problem: str  # What the user first asked
    resolved: bool = Field(default=False)  # Did we resolve it?
    was_helpful: bool = Field(default=False)  # Was the solution helpful?
    resolution_type: Optional[str] = None  # 'kb_article', 'web_search', 'pre_trained', etc.
    article_id: Optional[int] = Field(default=None, foreign_key="supportarticle.id")  # Which article helped
    escalated_to_ticket: bool = Field(default=False)  # Did they create a ticket?
    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    
    # Enhanced tracking
    conversation_json: Optional[str] = None  # Full conversation history as JSON
    issue_category: Optional[str] = None  # Detected issue category
    device_type: Optional[str] = None  # computer, printer, phone, etc.
    frustration_level: int = Field(default=0)  # 0-5, detected from tone
    steps_tried: Optional[str] = None  # JSON list of troubleshooting steps already tried
    total_messages: int = Field(default=0)  # Count of messages in conversation
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None  # Track activity


class SupportCategory(SQLModel, table=True):
    """Categories for organizing support articles"""
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    name: str  # e.g., "Printer Issues", "Network Problems"
    icon: str = Field(default="fas fa-question-circle")  # FontAwesome icon
    description: Optional[str] = None
    article_count: int = Field(default=0)  # Cached count
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
