"""
IT Knowledge Base seed data package.

Contains comprehensive troubleshooting articles and diagnostic trees
organized by category.  Each sub-module exports:
  - ARTICLES  : list[dict]   – article definitions
  - DIAGNOSTIC_TREE : dict  – interactive diagnostic tree
"""

from app.core.kb_data.printer import ARTICLES as _printer_a, DIAGNOSTIC_TREE as _printer_t
from app.core.kb_data.windows import ARTICLES as _windows_a, DIAGNOSTIC_TREE as _windows_t
from app.core.kb_data.network import ARTICLES as _network_a, DIAGNOSTIC_TREE as _network_t
from app.core.kb_data.email import ARTICLES as _email_a, DIAGNOSTIC_TREE as _email_t
from app.core.kb_data.hardware import ARTICLES as _hardware_a, DIAGNOSTIC_TREE as _hardware_t
from app.core.kb_data.software import ARTICLES as _software_a, DIAGNOSTIC_TREE as _software_t
from app.core.kb_data.auth import ARTICLES as _auth_a, DIAGNOSTIC_TREE as _auth_t
from app.core.kb_data.server import ARTICLES as _server_a, DIAGNOSTIC_TREE as _server_t
from app.core.kb_data.security import ARTICLES as _security_a, DIAGNOSTIC_TREE as _security_t
from app.core.kb_data.mobile import ARTICLES as _mobile_a, DIAGNOSTIC_TREE as _mobile_t
from app.core.kb_data.cloud import ARTICLES as _cloud_a, DIAGNOSTIC_TREE as _cloud_t
from app.core.kb_data.backup_recovery import ARTICLES as _backup_a, DIAGNOSTIC_TREE as _backup_t

# ── Combined exports ───────────────────────────────────────────────

ALL_ARTICLES: list[dict] = (
    _printer_a + _windows_a + _network_a + _email_a
    + _hardware_a + _software_a + _auth_a + _server_a
    + _security_a + _mobile_a + _cloud_a + _backup_a
)

ALL_DIAGNOSTIC_TREES: list[dict] = [
    _printer_t, _windows_t, _network_t, _email_t,
    _hardware_t, _software_t, _auth_t, _server_t,
    _security_t, _mobile_t, _cloud_t, _backup_t,
]

# Category definitions with icons for the UI
CATEGORIES: list[dict] = [
    {"name": "Printer", "icon": "fas fa-print", "description": "Printer and print server troubleshooting"},
    {"name": "Windows", "icon": "fab fa-windows", "description": "Windows OS issues, BSOD, updates, and system errors"},
    {"name": "Network", "icon": "fas fa-network-wired", "description": "Network connectivity, Wi-Fi, DNS, and VPN issues"},
    {"name": "Email & Outlook", "icon": "fas fa-envelope", "description": "Outlook, Exchange, and email client problems"},
    {"name": "Hardware", "icon": "fas fa-microchip", "description": "Monitor, USB, audio, keyboard, mouse, and hardware failures"},
    {"name": "Software", "icon": "fas fa-cube", "description": "Application errors, installation, compatibility, and crashes"},
    {"name": "Account & Access", "icon": "fas fa-key", "description": "Login, password, MFA, Active Directory, and access issues"},
    {"name": "Server", "icon": "fas fa-server", "description": "Server administration, AD, DNS, DHCP, and infrastructure"},
    {"name": "Security", "icon": "fas fa-shield-alt", "description": "Malware, ransomware, phishing, firewall, and incident response"},
    {"name": "Mobile & Phone", "icon": "fas fa-mobile-alt", "description": "Mobile device management, email sync, and phone issues"},
    {"name": "Cloud & M365", "icon": "fas fa-cloud", "description": "Microsoft 365, SharePoint, OneDrive, Azure AD, and cloud services"},
    {"name": "Backup & Recovery", "icon": "fas fa-database", "description": "Backup strategies, data recovery, disaster recovery, and restore"},
]
