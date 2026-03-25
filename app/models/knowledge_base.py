"""
IT Knowledge Base Models
- Diagnostic trees with step-by-step follow-up questions
- Resolved cases logged by technicians
- Tags for filtering
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column, Text


class KBDiagnosticTree(SQLModel, table=True):
    """
    Decision-tree nodes for interactive diagnostics.
    Each node is either a QUESTION (with child nodes) or a SOLUTION (leaf).
    
    Example tree:
      "Printer not printing" (root question)
        -> "Wi-Fi or USB?" (follow-up question)
            -> "Wi-Fi" -> solution: "Check wireless connection..."
            -> "USB"  -> solution: "Check cable is plugged in..."
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    
    # Tree structure
    parent_id: Optional[int] = Field(default=None, foreign_key="kbdiagnostictree.id", index=True)
    
    # Node content
    title: str  # Short label, e.g. "Printer not printing" or "Wi-Fi" or "USB"
    node_type: str = Field(default="question", index=True)  # "question" | "option" | "solution"
    question_text: Optional[str] = Field(default=None, sa_column=Column(Text))  # Full question to display
    solution_text: Optional[str] = Field(default=None, sa_column=Column(Text))  # Solution steps if leaf node
    
    # Metadata
    category: str = Field(default="general", index=True)  # e.g. printer, network, software
    tags: Optional[str] = None  # Comma-separated tags
    sort_order: int = Field(default=0)  # Ordering among siblings
    
    # Management
    is_active: bool = Field(default=True)
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class KBResolvedCase(SQLModel, table=True):
    """
    Technician-submitted resolved cases — crowdsourced knowledge base.
    Each entry describes a problem they encountered and how they fixed it.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id", index=True)
    
    # Problem description
    problem_title: str  # e.g. "HP LaserJet not printing over Wi-Fi"
    problem_description: str = Field(sa_column=Column(Text))  # Detailed description
    error_message: Optional[str] = None  # Exact error text if applicable
    
    # Classification
    category: str = Field(default="general", index=True)
    device_type: Optional[str] = None  # printer, laptop, server, phone, etc.
    device_brand: Optional[str] = None  # HP, Dell, Lenovo, etc.
    device_model: Optional[str] = None  # Specific model
    connection_type: Optional[str] = None  # wifi, cable, bluetooth, vpn, etc.
    tags: Optional[str] = None  # Comma-separated: #network, #hardware, #auth
    
    # Resolution
    solution_steps: str = Field(sa_column=Column(Text))  # Step-by-step how they fixed it
    root_cause: Optional[str] = Field(default=None, sa_column=Column(Text))  # What was the underlying cause
    time_to_resolve: Optional[int] = None  # Minutes it took
    
    # Source ticket link (optional — no FK constraint, ticket may be in tasks table)
    ticket_id: Optional[int] = Field(default=None, index=True)
    ticket_number: Optional[str] = None  # e.g. TKT-2026-00933
    
    # Helpfulness tracking
    times_viewed: int = Field(default=0)
    helpful_votes: int = Field(default=0)
    not_helpful_votes: int = Field(default=0)
    
    # Management
    is_verified: bool = Field(default=False)  # Admin-verified
    resolved_by_id: int = Field(foreign_key="user.id", index=True)
    resolved_by_name: Optional[str] = None  # Cached for display
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
