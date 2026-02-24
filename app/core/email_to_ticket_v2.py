"""
Email-to-Ticket Service V2
IMAP-based email processing, uses database settings, keeps emails on server
"""

import asyncio
import imaplib
import email
import socket
from email.header import decode_header
from email.utils import parseaddr
import re
import logging
from datetime import datetime, date, timezone, timedelta
from typing import Optional, List, Tuple

# Set default IMAP socket timeout to prevent hanging connections
IMAP_TIMEOUT = 60  # seconds
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.ticket import Ticket, TicketHistory, TicketComment
from app.models.user import User
from app.models.notification import Notification
from app.models.email_settings import EmailSettings
from app.models.processed_mail import ProcessedMail
from app.models.project import Project

# Setup logger
logger = logging.getLogger(__name__)

# Timezone offset (UTC+2 for South Africa)
LOCAL_TZ_OFFSET = timedelta(hours=2)

def get_local_time() -> datetime:
    """Get current time in local timezone (UTC+2)"""
    return datetime.now(timezone(LOCAL_TZ_OFFSET))


def is_support_query(subject: str, body: str, sender_email: str) -> bool:
    """
    Analyze if an email looks like a support query.
    Used for filtering spam/junk folder emails.
    
    Returns True if the email appears to be a legitimate support request.
    """
    content = (subject + ' ' + body).lower()
    sender = sender_email.lower()
    
    # Keywords that indicate a support query
    support_keywords = [
        'help', 'support', 'issue', 'problem', 'error', 'broken', 'not working',
        'urgent', 'please', 'assist', 'request', 'ticket', 'query', 'question',
        'fix', 'repair', 'service', 'maintenance', 'install', 'setup', 'configure',
        'password', 'login', 'access', 'account', 'printer', 'computer', 'laptop',
        'network', 'internet', 'email', 'phone', 'call', 'meeting', 'appointment',
        'invoice', 'quote', 'order', 'delivery', 'payment', 'refund',
        'complaint', 'feedback', 'suggestion', 'thank you', 'thanks',
        're:', 'fwd:', 'reply', 'response', 'follow up', 'following up',
        'tkt-', 'ticket #', 'case #', 'reference'
    ]
    
    # Spam indicators - if too many, skip this email
    spam_keywords = [
        'unsubscribe', 'click here', 'act now', 'limited time', 'free gift',
        'congratulations', 'you won', 'lottery', 'inheritance', 'million dollars',
        'viagra', 'cialis', 'pharmacy', 'weight loss', 'diet pill',
        'nigerian prince', 'wire transfer', 'western union', 'bitcoin',
        'cryptocurrency', 'investment opportunity', 'double your money',
        'no obligation', 'risk free', 'guaranteed', 'special offer',
        'dear friend', 'dear customer', 'dear sir/madam'
    ]
    
    # Known spam sender patterns
    spam_sender_patterns = [
        'noreply@', 'no-reply@', 'mailer-daemon', 'postmaster',
        'bounce', 'newsletter', 'marketing', 'promo', 'sales@',
        'info@', 'admin@', 'support@' # Generic addresses often used by spam
    ]
    
    # Count support indicators
    support_score = sum(1 for kw in support_keywords if kw in content)
    
    # Count spam indicators
    spam_score = sum(1 for kw in spam_keywords if kw in content)
    spam_score += sum(1 for pattern in spam_sender_patterns if pattern in sender)
    
    # Check for personal greeting (indicates real email)
    has_personal_greeting = any(greeting in content for greeting in [
        'hi ', 'hello ', 'dear ', 'good morning', 'good afternoon', 'good day'
    ])
    if has_personal_greeting:
        support_score += 2
    
    # If it looks like a reply to a ticket, it's definitely support
    if 'tkt-' in content or 'ticket #' in content:
        return True
    
    # Decision: needs more support indicators than spam indicators
    # and at least 2 support keywords to be considered a support query
    return support_score >= 2 and support_score > spam_score


async def generate_unique_ticket_number(db: AsyncSession, workspace_id: int) -> str:
    """Generate a unique ticket number by finding the max existing number GLOBALLY"""
    from sqlalchemy import func
    
    current_year = datetime.now().year
    prefix = f"TKT-{current_year}-"
    
    # Find the highest ticket number for this year GLOBALLY (across all workspaces)
    # because ticket_number is unique across the entire database
    result = await db.execute(
        select(Ticket.ticket_number)
        .where(Ticket.ticket_number.like(f"{prefix}%"))
    )
    existing_numbers = result.scalars().all()
    
    max_num = 0
    for tn in existing_numbers:
        try:
            # Extract the number part (e.g., "TKT-2025-00042" -> 42)
            num_part = int(tn.replace(prefix, ""))
            if num_part > max_num:
                max_num = num_part
        except (ValueError, AttributeError):
            continue
    
    # Generate next number
    next_num = max_num + 1
    return f"{prefix}{next_num:05d}"


class EmailToTicketService:
    """Service to process emails from IMAP and create tickets"""
    
    def __init__(self, email_settings: EmailSettings, workspace_id: int):
        self.settings = email_settings
        self.workspace_id = workspace_id
        
    def connect_imap(self):
        """Connect to IMAP server with timeout"""
        try:
            # Set socket timeout to prevent hanging
            socket.setdefaulttimeout(IMAP_TIMEOUT)
            
            if self.settings.incoming_mail_use_ssl:
                mail = imaplib.IMAP4_SSL(
                    self.settings.incoming_mail_host,
                    self.settings.incoming_mail_port or 993,
                    timeout=IMAP_TIMEOUT
                )
            else:
                mail = imaplib.IMAP4(
                    self.settings.incoming_mail_host,
                    self.settings.incoming_mail_port or 143
                )
            
            # Reset default timeout after connection
            socket.setdefaulttimeout(None)
            
            mail.login(
                self.settings.incoming_mail_username,
                self.settings.incoming_mail_password
            )
            return mail
        except Exception as e:
            print(f"Failed to connect to IMAP server: {e}")
            raise
    
    def _fetch_raw_emails_sync(self) -> List[dict]:
        """
        Synchronous method to fetch raw emails from IMAP server.
        This runs in a thread pool to avoid blocking the event loop.
        
        Returns list of dicts with: email_id, msg_bytes, message_id
        """
        raw_emails = []
        mail = None
        
        try:
            mail = self.connect_imap()
            mail.select('INBOX')
            
            # Search for emails from the last 7 days (not just unread)
            # This ensures we catch emails even if they're marked as read by other clients
            from datetime import datetime, timedelta
            date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
            status, messages = mail.search(None, f'SINCE {date_since}')
            email_ids = messages[0].split()
            
            print(f"[IMAP] Found {len(email_ids)} messages from last 7 days")
            
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if msg_data and msg_data[0]:
                        raw_emails.append({
                            'email_id': email_id,
                            'msg_bytes': msg_data[0][1],
                            'mail': mail  # Pass mail connection for marking as read later
                        })
                except Exception as e:
                    print(f"[IMAP] Error fetching email {email_id}: {e}")
                    continue
            
            # Don't close here - we need to mark emails as read later
            return raw_emails
            
        except Exception as e:
            print(f"[IMAP] Error connecting to IMAP: {e}")
            if mail:
                try:
                    mail.close()
                    mail.logout()
                except:
                    pass
            return []
    
    def decode_header_value(self, header: str) -> str:
        """Decode email header"""
        if not header:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part
        
        return decoded_string
    
    def extract_email_address(self, from_header: str) -> Tuple[str, str]:
        """Extract name and email from 'From' header"""
        name, email_addr = parseaddr(from_header)
        return name, email_addr.lower()
    
    def clean_email_body(self, body: str) -> str:
        """Clean email body (format nicely but preserve signature content)"""
        import re
        
        lines = body.split('\n')
        cleaned_lines = []
        in_quoted_reply = False
        
        # Markers that indicate start of quoted reply (not signature)
        quote_markers = [
            'On ', 'From:', '-----Original Message-----',
            '> On ', '> From:', 'wrote:'
        ]
        
        for line in lines:
            stripped = line.strip()
            
            # Detect start of quoted reply section (usually previous email thread)
            if any(stripped.startswith(marker) for marker in quote_markers):
                # Check if this looks like a quote header
                if 'wrote:' in stripped or stripped.startswith('From:') or stripped.startswith('-----'):
                    in_quoted_reply = True
                    continue
            
            # Skip lines that are clearly quoted text (start with >)
            if stripped.startswith('>'):
                continue
            
            # If we're in a quoted reply section, skip until we see a non-quoted line
            if in_quoted_reply and stripped:
                # Still in quote section
                continue
            elif in_quoted_reply and not stripped:
                # Empty line might end quote section, but be careful
                pass
            
            cleaned_lines.append(line)
        
        result = '\n'.join(cleaned_lines).strip()
        
        # Clean up excessive whitespace 
        result = re.sub(r'\n{4,}', '\n\n\n', result)  # Max 3 consecutive newlines
        
        return result
    
    def determine_priority(self, subject: str, body: str) -> str:
        """Auto-detect priority from content"""
        content = (subject + ' ' + body).lower()
        
        urgent_keywords = ['urgent', 'emergency', 'critical', 'asap', 'down', 'not working']
        high_keywords = ['important', 'high priority', 'soon', 'broken', 'error']
        
        if any(keyword in content for keyword in urgent_keywords):
            return 'urgent'
        elif any(keyword in content for keyword in high_keywords):
            return 'high'
        else:
            return 'medium'
    
    def extract_email_body(self, msg) -> str:
        """Extract plain text body from email message, converting HTML if needed"""
        body = ""
        html_body = ""
        
        if msg.is_multipart():
            # Try to get both plain text and HTML versions
            for part in msg.walk():
                content_type = part.get_content_type()
                
                if content_type == "text/plain" and not body:
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        body = payload.decode(charset, errors='ignore')
                    except:
                        continue
                
                elif content_type == "text/html" and not html_body:
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        html_body = payload.decode(charset, errors='ignore')
                    except:
                        continue
        else:
            content_type = msg.get_content_type()
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                decoded = payload.decode(charset, errors='ignore')
                
                if content_type == "text/html":
                    html_body = decoded
                else:
                    body = decoded
            except:
                body = str(msg.get_payload())
        
        # If we only have HTML, convert it to plain text
        if not body and html_body:
            body = self.html_to_text(html_body)
        elif not body:
            body = "No content"
        
        return self.clean_email_body(body)
    
    def html_to_text(self, html: str) -> str:
        """Convert HTML email to clean plain text, preserving signature layout"""
        from html.parser import HTMLParser
        import re
        
        class HTMLToText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False
                self.current_href = None
                self.link_text = []
                self.in_link = False
                self.last_was_block = False
                
            def handle_starttag(self, tag, attrs):
                attrs_dict = dict(attrs)
                if tag in ['script', 'style', 'head']:
                    self.skip = True
                elif tag == 'br':
                    self.text.append('\n')
                    self.last_was_block = True
                elif tag == 'p':
                    if self.text and not self.last_was_block:
                        self.text.append('\n')
                    self.last_was_block = True
                elif tag == 'div':
                    if self.text and not self.last_was_block:
                        self.text.append('\n')
                    self.last_was_block = True
                elif tag in ['li']:
                    self.text.append('\n• ')
                    self.last_was_block = True
                elif tag == 'a':
                    self.current_href = attrs_dict.get('href', '')
                    self.in_link = True
                    self.link_text = []
                elif tag == 'hr':
                    self.text.append('\n' + '—' * 30 + '\n')
                    self.last_was_block = True
                elif tag == 'tr':
                    # New table row = new line
                    if self.text and not self.last_was_block:
                        self.text.append('\n')
                    self.last_was_block = True
                elif tag in ['td', 'th']:
                    # Table cells separated by a space (not pipes)
                    if self.text and self.text[-1] not in ['\n', '']:
                        last = self.text[-1].rstrip()
                        if last:
                            self.text.append('  ')
                elif tag == 'img':
                    # Show alt text for images (e.g. logo alt text)
                    alt = attrs_dict.get('alt', '').strip()
                    if alt:
                        self.text.append(alt)
                        self.last_was_block = False
                elif tag == 'blockquote':
                    self.text.append('\n')
                    self.last_was_block = True
                    
            def handle_endtag(self, tag):
                if tag in ['script', 'style', 'head']:
                    self.skip = False
                elif tag == 'a':
                    # Smart URL handling
                    href = self.current_href or ''
                    display = ''.join(self.link_text).strip()
                    
                    if href.startswith('mailto:'):
                        email_addr = href.replace('mailto:', '').split('?')[0]
                        # If link text is the same as the email, just show it once
                        if display and display != email_addr:
                            self.text.append(f'{display} ({email_addr})')
                        else:
                            self.text.append(email_addr)
                    elif href.startswith(('http://', 'https://')):
                        if display and display != href and not display.startswith('http'):
                            # Link text is meaningful (not just the URL)
                            self.text.append(f'{display} ({href})')
                        elif display:
                            # Link text IS the URL or similar - just show once
                            self.text.append(display)
                        else:
                            self.text.append(href)
                    elif display:
                        self.text.append(display)
                        
                    self.current_href = None
                    self.in_link = False
                    self.link_text = []
                    self.last_was_block = False
                elif tag in ['p', 'div', 'blockquote']:
                    if self.text and not self.last_was_block:
                        self.text.append('\n')
                    self.last_was_block = True
                elif tag == 'tr':
                    pass  # handled in starttag
                elif tag in ['table']:
                    if self.text and not self.last_was_block:
                        self.text.append('\n')
                    self.last_was_block = True
                elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    self.text.append('\n')
                    self.last_was_block = True
                    
            def handle_data(self, data):
                if not self.skip:
                    cleaned = data.strip()
                    if cleaned:
                        if self.in_link:
                            self.link_text.append(cleaned)
                        else:
                            self.text.append(cleaned)
                        self.last_was_block = False
                    elif data and not self.last_was_block:
                        # Whitespace between inline elements
                        if self.text and self.text[-1] not in ['\n', '\n\n', '']:
                            self.text.append(' ')
        
        try:
            parser = HTMLToText()
            parser.feed(html)
            text = ''.join(parser.text)
            
            # Clean up extra whitespace but preserve signature formatting
            text = re.sub(r'\n{4,}', '\n\n', text)      # Max 2 consecutive newlines
            text = re.sub(r' {3,}', '  ', text)          # Max 2 consecutive spaces
            text = re.sub(r'\t+', ' ', text)              # Tabs to space
            text = re.sub(r'[ \t]+\n', '\n', text)        # Trailing whitespace on lines
            text = re.sub(r'\n[ \t]+\n', '\n\n', text)    # Lines with only whitespace
            text = text.strip()
            
            return text
        except Exception as e:
            print(f"Error converting HTML to text: {e}")
            # Fallback: strip all HTML tags
            return re.sub(r'<[^>]+>', '', html)
    
    async def is_email_processed(self, db: AsyncSession, message_id: str) -> bool:
        """Check if email was already processed (globally, not workspace-specific)"""
        # Check globally - if ANY system processed this email, skip it
        result = await db.execute(
            select(ProcessedMail).where(
                ProcessedMail.message_id == message_id
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def find_ticket_by_reply(self, db: AsyncSession, in_reply_to: str, references: str) -> Optional[Ticket]:
        """Find ticket from reply headers (In-Reply-To or References)"""
        print(f"[DEBUG] find_ticket_by_reply called with:")
        print(f"[DEBUG]   in_reply_to: '{in_reply_to}'")
        print(f"[DEBUG]   references: '{references}'")
        print(f"[DEBUG]   workspace_id: {self.workspace_id}")
        
        # Try In-Reply-To first
        if in_reply_to:
            print(f"[DEBUG] Searching processedmail for message_id: '{in_reply_to}'")
            result = await db.execute(
                select(ProcessedMail).where(
                    ProcessedMail.message_id == in_reply_to,
                    ProcessedMail.workspace_id == self.workspace_id
                )
            )
            processed = result.scalar_one_or_none()
            print(f"[DEBUG] ProcessedMail result: {processed}")
            if processed and processed.ticket_id:
                print(f"[DEBUG] Found ticket_id: {processed.ticket_id}")
                ticket_result = await db.execute(
                    select(Ticket).where(Ticket.id == processed.ticket_id)
                )
                ticket = ticket_result.scalar_one_or_none()
                if ticket and ticket.status in ['closed', 'resolved']:
                    print(f"[DEBUG] Found ticket #{ticket.ticket_number} but it's CLOSED - will create new ticket")
                    return None
                print(f"[DEBUG] Returning ticket: {ticket.ticket_number if ticket else None}")
                return ticket
        
        # Try References (can contain multiple message IDs)
        if references:
            print(f"[DEBUG] Trying References header")
            # References format: "<msg1> <msg2> <msg3>"
            ref_ids = references.strip().split()
            print(f"[DEBUG] Parsed reference IDs: {ref_ids}")
            for ref_id in reversed(ref_ids):  # Check from newest to oldest
                # Keep angle brackets for matching
                ref_id = ref_id.strip()
                print(f"[DEBUG] Checking reference: '{ref_id}'")
                result = await db.execute(
                    select(ProcessedMail).where(
                        ProcessedMail.message_id == ref_id,
                        ProcessedMail.workspace_id == self.workspace_id
                    )
                )
                processed = result.scalar_one_or_none()
                if processed and processed.ticket_id:
                    ticket_result = await db.execute(
                        select(Ticket).where(Ticket.id == processed.ticket_id)
                    )
                    ticket = ticket_result.scalar_one_or_none()
                    if ticket and ticket.status in ['closed', 'resolved']:
                        print(f"[DEBUG] Found ticket #{ticket.ticket_number} via References but it's CLOSED - will create new ticket")
                        continue  # Try next reference
                    print(f"[DEBUG] Found ticket via References: {ticket.ticket_number if ticket else None}")
                    return ticket
        
        print(f"[DEBUG] No ticket found via In-Reply-To or References")
        return None
    
    async def find_ticket_by_subject(self, db: AsyncSession, subject: str) -> Optional[Ticket]:
        """
        Fallback: Find ticket by subject line pattern
        Gmail/Outlook include "Re: Ticket #12345" or "Ticket #12345" in subject
        """
        import re
        
        print(f"[DEBUG] Trying to find ticket by subject: '{subject}'")
        
        # Clean up the subject - remove Re:, Fwd:, etc.
        clean_subject = re.sub(r'^(Re:|RE:|Fwd:|FWD:|\[.*?\])\s*', '', subject, flags=re.IGNORECASE).strip()
        print(f"[DEBUG] Cleaned subject: '{clean_subject}'")
        
        # Look for patterns like "Ticket #12345" or "#12345"
        patterns = [
            r'Ticket\s*#?\s*(\d+)',      # "Ticket #12345" or "Ticket 12345"
            r'Re:\s*Ticket\s*#?\s*(\d+)', # "Re: Ticket #12345"
            r'#(\d+)',                     # "#12345" anywhere
            r'\bticket\s*#?\s*(\d+)',      # "ticket 12345" (case insensitive)
            r'\[#(\d+)\]',                 # "[#12345]"
            r'(?:^|\s)(\d{5,})',           # 5+ digit number (likely ticket number)
        ]
        
        # Try on both original and cleaned subject
        for test_subject in [subject, clean_subject]:
            for pattern in patterns:
                match = re.search(pattern, test_subject, re.IGNORECASE)
                if match:
                    ticket_number = match.group(1)
                    print(f"[DEBUG] Found potential ticket number in subject: {ticket_number} (pattern: {pattern})")
                    
                    # Search for ticket by number
                    result = await db.execute(
                        select(Ticket).where(
                            Ticket.ticket_number == ticket_number,
                            Ticket.workspace_id == self.workspace_id
                        )
                    )
                    ticket = result.scalar_one_or_none()
                    if ticket:
                        # Don't add comments to closed tickets - create new ticket instead
                        if ticket.status in ['closed', 'resolved']:
                            print(f"[DEBUG] Found ticket #{ticket.ticket_number} but it's CLOSED - will create new ticket")
                            return None
                        print(f"[DEBUG] ✅ Found ticket #{ticket.ticket_number} via subject line")
                        return ticket
                    else:
                        print(f"[DEBUG] Pattern matched '{ticket_number}' but no ticket found in database")
        
        print(f"[DEBUG] ❌ No ticket number found in subject")
        return None
    
    async def find_ticket_by_sender(self, db: AsyncSession, sender_email: str) -> Optional[Ticket]:
        """
        Last resort fallback: Find most recent open ticket from this sender
        Only matches if there's exactly ONE open ticket from this email
        """
        print(f"[DEBUG] Trying to find ticket by sender email: '{sender_email}'")
        
        # Search for open tickets from this email (not closed)
        result = await db.execute(
            select(Ticket).where(
                Ticket.guest_email == sender_email,
                Ticket.workspace_id == self.workspace_id,
                Ticket.status.in_(['new', 'open', 'pending', 'in_progress'])
            ).order_by(Ticket.created_at.desc())
        )
        tickets = result.scalars().all()
        
        if len(tickets) == 1:
            # Only auto-match if there's exactly one open ticket
            print(f"[DEBUG] ✅ Found single open ticket #{tickets[0].ticket_number} from sender")
            return tickets[0]
        elif len(tickets) > 1:
            print(f"[DEBUG] Found {len(tickets)} open tickets from sender - ambiguous, creating new ticket")
        else:
            print(f"[DEBUG] No open tickets found from sender")
        
        return None
    
    async def mark_email_processed(
        self, 
        db: AsyncSession, 
        message_id: str, 
        email_from: str, 
        subject: str, 
        ticket_id: int
    ):
        """Mark email as processed - with duplicate protection"""
        try:
            processed = ProcessedMail(
                message_id=message_id,
                email_from=email_from,
                subject=subject,
                ticket_id=ticket_id,
                workspace_id=self.workspace_id,
                processed_at=get_local_time()
            )
            db.add(processed)
            await db.commit()
        except Exception as e:
            # Handle duplicate key error gracefully (already processed by another worker)
            if 'UNIQUE constraint' in str(e) or 'duplicate' in str(e).lower():
                print(f"[IMAP] Email already marked as processed (race condition handled): {message_id[:50]}")
                await db.rollback()
            else:
                raise
    
    async def find_project_by_email(self, db: AsyncSession, to_email: str) -> Optional[Project]:
        """Find project by support email address"""
        if not to_email:
            return None
        
        to_email = to_email.lower().strip()
        print(f"[DEBUG] Looking for project with support_email: {to_email}")
        
        result = await db.execute(
            select(Project).where(
                Project.workspace_id == self.workspace_id,
                Project.support_email == to_email,
                Project.is_archived == False
            )
        )
        project = result.scalar_one_or_none()
        
        if project:
            print(f"[DEBUG] Found project: {project.name} (ID: {project.id})")
        else:
            print(f"[DEBUG] No project found for email: {to_email}")
        
        return project
    
    async def create_ticket_from_email(
        self,
        db: AsyncSession,
        sender_name: str,
        sender_email: str,
        subject: str,
        body: str,
        to_email: Optional[str] = None,
        project: Optional[Project] = None
    ) -> Ticket:
        """Create a guest ticket from email"""
        
        # Generate unique ticket number
        ticket_number = await generate_unique_ticket_number(db, self.workspace_id)
        
        # Determine priority
        priority = self.determine_priority(subject, body)
        
        # Create ticket
        ticket = Ticket(
            ticket_number=ticket_number,
            subject=subject[:200],  # Limit subject length
            description=body[:5000],  # Limit body length
            priority=priority,
            status='open',
            category='support',
            workspace_id=self.workspace_id,
            created_by_id=None,  # Guest ticket
            is_guest=True,
            guest_name=sender_name.split()[0] if sender_name else "Unknown",
            guest_surname=sender_name.split()[-1] if sender_name and len(sender_name.split()) > 1 else "",
            guest_email=sender_email,
            guest_phone="",
            guest_company="",
            guest_branch="",
            related_project_id=project.id if project else None,  # Link to project if found
            created_at=get_local_time(),
            updated_at=get_local_time()
        )
        
        db.add(ticket)
        await db.flush()
        
        # Add history entry
        history_comment = f'Ticket created automatically from email: {sender_email}'
        if project:
            history_comment += f' → Project: {project.name}'
        if to_email:
            history_comment += f' (to: {to_email})'
            
        history = TicketHistory(
            ticket_id=ticket.id,
            user_id=None,  # System action
            action='created',
            comment=history_comment,
            created_at=datetime.utcnow()
        )
        db.add(history)
        
        # Notify all admins about new email ticket
        from app.models.notification import Notification
        from app.models.user import User
        from sqlmodel import select as sql_select
        
        admin_users = (await db.execute(
            sql_select(User).where(User.workspace_id == self.workspace_id).where(User.is_admin == True)
        )).scalars().all()
        
        notification_message = f'New ticket from email #{ticket_number}: {subject[:100]}'
        if project:
            notification_message = f'New ticket for {project.name} from email #{ticket_number}: {subject[:100]}'
        
        for admin in admin_users:
            # Check if admin has muted ticket notifications
            if getattr(admin, 'mute_ticket_notifications', False):
                continue
            notification = Notification(
                user_id=admin.id,
                type='ticket',
                message=notification_message,
                url=f'/web/tickets/{ticket.id}',
                related_id=ticket.id
            )
            db.add(notification)
        
        await db.commit()
        await db.refresh(ticket)
        
        return ticket
    
    async def add_comment_from_email(
        self,
        db: AsyncSession,
        ticket: Ticket,
        sender_name: str,
        sender_email: str,
        body: str
    ) -> TicketComment:
        """Add a comment to an existing ticket from email reply"""
        
        # Create comment
        comment = TicketComment(
            ticket_id=ticket.id,
            user_id=None,  # Guest comment from email
            content=f"**Email reply from {sender_name} ({sender_email}):**\n\n{body}",
            is_internal=False,
            created_at=get_local_time()
        )
        db.add(comment)
        
        # Update ticket timestamp
        ticket.updated_at = get_local_time()
        
        # Add history entry
        history = TicketHistory(
            ticket_id=ticket.id,
            user_id=None,
            action='comment_added',
            comment=f'Email reply received from {sender_email}',
            created_at=get_local_time()
        )
        db.add(history)
        
        # Notify all non-admin users in the workspace about email reply
        from app.models.user import User
        from sqlmodel import select
        
        # Get all non-admin users in the workspace
        users_query = (
            select(User)
            .where(User.workspace_id == ticket.workspace_id)
            .where(User.is_admin == False)
        )
        non_admin_users = (await db.execute(users_query)).scalars().all()
        
        # Create notification for each non-admin user (if they haven't muted)
        for user in non_admin_users:
            # Check if user has muted ticket notifications
            if getattr(user, 'mute_ticket_notifications', False):
                continue
            notification = Notification(
                user_id=user.id,
                type='email_reply',
                message=f'📧 Email reply received on ticket #{ticket.ticket_number} from {sender_email}',
                url=f'/web/tickets/{ticket.id}',
                related_id=ticket.id
            )
            db.add(notification)
        
        await db.commit()
        await db.refresh(comment)
        
        return comment
    
    async def fetch_imap_emails(self, db: AsyncSession) -> List[Ticket]:
        """Fetch emails from IMAP server and create tickets.
        
        Uses asyncio.to_thread() to run blocking IMAP operations in a thread pool,
        preventing the event loop from blocking and keeping the website responsive.
        """
        tickets_created = []
        mail = None
        
        try:
            # Run blocking IMAP connection in a thread pool
            def connect_and_fetch():
                """Synchronous function to connect and fetch emails from all folders"""
                nonlocal mail
                mail = self.connect_imap()
                
                # Folders to check - INBOX gets all emails, others are filtered for support queries
                folders_to_check = [
                    ('INBOX', False),  # (folder_name, requires_analysis)
                    ('[Gmail]/Spam', True),
                    ('[Gmail]/Trash', True),
                    ('Spam', True),
                    ('Junk', True),
                    ('Trash', True),
                    ('INBOX.Spam', True),
                    ('INBOX.Junk', True),
                    ('INBOX.Trash', True),
                ]
                
                all_raw_emails = []
                
                for folder_name, requires_analysis in folders_to_check:
                    try:
                        status, _ = mail.select(folder_name)
                        if status != 'OK':
                            continue
                        
                        # Search for emails from the last 7 days
                        from datetime import datetime, timedelta
                        date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
                        status, messages = mail.search(None, f'SINCE {date_since}')
                        email_ids = messages[0].split()
                        
                        if email_ids:
                            print(f"[IMAP] Found {len(email_ids)} messages in {folder_name}")
                        
                        for email_id in email_ids:
                            try:
                                status, msg_data = mail.fetch(email_id, '(RFC822)')
                                if msg_data and msg_data[0]:
                                    all_raw_emails.append({
                                        'email_id': email_id,
                                        'msg_bytes': msg_data[0][1],
                                        'folder': folder_name,
                                        'requires_analysis': requires_analysis
                                    })
                            except Exception as e:
                                print(f"[IMAP] Error fetching email {email_id} from {folder_name}: {e}")
                                continue
                    except Exception as e:
                        # Folder doesn't exist or can't be selected - skip silently
                        continue
                
                # Re-select INBOX for marking emails as read
                mail.select('INBOX')
                return all_raw_emails
            
            # Run IMAP fetch in thread pool (non-blocking)
            raw_emails = await asyncio.to_thread(connect_and_fetch)
            
            print(f"[IMAP] Found {len(raw_emails)} messages from last 7 days")
            
            # Import for fresh sessions
            from sqlmodel.ext.asyncio.session import AsyncSession as NewAsyncSession
            from app.core.database import engine
            
            # Process each email with fresh db sessions to avoid greenlet issues
            for raw_email in raw_emails:
                email_id = raw_email['email_id']
                folder = raw_email.get('folder', 'INBOX')
                requires_analysis = raw_email.get('requires_analysis', False)
                try:
                    msg = email.message_from_bytes(raw_email['msg_bytes'])
                    
                    # Get message ID
                    message_id = msg.get('Message-ID', f'no-id-{email_id.decode()}')
                    
                    # Use fresh session for each email to avoid greenlet context issues
                    async with NewAsyncSession(engine) as fresh_db:
                        # Check if already processed
                        if await self.is_email_processed(fresh_db, message_id):
                            # Mark as read but don't process again (run in thread)
                            await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                            continue
                        
                        # Extract email info
                        from_header = msg.get('From', '')
                        sender_name, sender_email = self.extract_email_address(from_header)
                        to_header = msg.get('To', '')
                        _, to_email = self.extract_email_address(to_header)
                        
                        subject = self.decode_header_value(msg.get('Subject', 'No Subject'))
                        body = self.extract_email_body(msg)
                        
                        print(f"\n{'='*80}")
                        print(f"[IMAP] Processing email from folder: {folder}")
                        print(f"[IMAP] From: {sender_name} <{sender_email}>")
                        print(f"[IMAP] To: {to_email}")
                        print(f"[IMAP] Subject: {subject}")
                        print(f"[IMAP] Message-ID: {message_id}")
                        
                        # Check if this is a reply to an existing ticket
                        # Keep Message-ID with angle brackets for matching
                        in_reply_to = msg.get('In-Reply-To', '').strip()
                        references = msg.get('References', '').strip()
                        
                        print(f"[IMAP] In-Reply-To: '{in_reply_to}'")
                        print(f"[IMAP] References: '{references}'")
                        
                        existing_ticket = await self.find_ticket_by_reply(fresh_db, in_reply_to, references)
                        
                        # If not found via headers, try by sender email
                        # (Skip subject matching - too aggressive, catches invoice numbers etc.)
                        if not existing_ticket:
                            print(f"[IMAP] Trying sender email fallback...")
                            existing_ticket = await self.find_ticket_by_sender(fresh_db, sender_email)
                        
                        if existing_ticket:
                            print(f"[IMAP] ✅ MATCH FOUND - Adding to ticket #{existing_ticket.ticket_number}")
                        else:
                            print(f"[IMAP] ❌ NO MATCH - Will create new ticket")
                        print(f"{'='*80}\n")
                        
                        # Find project by support email
                        project = await self.find_project_by_email(fresh_db, to_email)
                        
                        if existing_ticket:
                            # Refresh to ensure all attributes are loaded
                            await fresh_db.refresh(existing_ticket)
                            existing_ticket_id = existing_ticket.id
                            existing_ticket_number = existing_ticket.ticket_number
                            
                            # Add as comment to existing ticket
                            await self.add_comment_from_email(
                                fresh_db, existing_ticket, sender_name, sender_email, body
                            )
                            
                            # Mark as processed
                            await self.mark_email_processed(
                                fresh_db, message_id, sender_email, subject, existing_ticket_id
                            )
                            
                            # Mark email as read (run in thread - blocking operation)
                            await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                            
                            print(f"[IMAP] Added comment to ticket {existing_ticket_number} from {sender_email}")
                        else:
                            # For spam/junk folders, check if this is a support query first
                            if requires_analysis:
                                if not is_support_query(subject, body, sender_email):
                                    print(f"[IMAP] ⏭️ SKIPPING: Email from {folder} folder doesn't look like a support query")
                                    print(f"[IMAP]    Subject: {subject[:50]}...")
                                    # Mark as read but don't create ticket
                                    await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                                    # Mark as processed to avoid checking again
                                    await self.mark_email_processed(
                                        fresh_db, message_id, sender_email, subject, None
                                    )
                                    continue
                                else:
                                    print(f"[IMAP] ✅ Email from {folder} folder looks like a support query - creating ticket")
                            
                            # Always create tickets (linked to project if matched)
                            ticket = await self.create_ticket_from_email(
                                fresh_db, sender_name, sender_email, subject, body, to_email, project
                            )
                            
                            # Refresh and store ID immediately
                            await fresh_db.refresh(ticket)
                            ticket_id = ticket.id
                            ticket_number = ticket.ticket_number
                            
                            # Mark as processed
                            await self.mark_email_processed(
                                fresh_db, message_id, sender_email, subject, ticket_id
                            )
                            
                            # Mark email as read (run in thread)
                            await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                            
                            tickets_created.append(ticket)
                            if project:
                                print(f"[IMAP] Created ticket {ticket_number} for project '{project.name}' from {sender_email} (folder: {folder})")
                            else:
                                print(f"[IMAP] Created ticket {ticket_number} from {sender_email} (folder: {folder})")
                    
                except Exception as e:
                    print(f"[IMAP] Error processing email {email_id}: {e}")
                    continue
            
            # Close connection in thread pool
            if mail:
                await asyncio.to_thread(lambda: (mail.close(), mail.logout()))
            
        except Exception as e:
            print(f"[IMAP] Error fetching emails: {e}")
            if mail:
                try:
                    await asyncio.to_thread(lambda: (mail.close(), mail.logout()))
                except:
                    pass
        
        return tickets_created
    
    async def process_emails(self, db: AsyncSession) -> List[Ticket]:
        """Process emails from IMAP server"""
        return await self.fetch_imap_emails(db)


async def process_workspace_emails(db: AsyncSession, workspace_id: int) -> List[Ticket]:
    """
    Process emails for a workspace using its email settings
    
    Args:
        db: Database session
        workspace_id: Workspace ID
        
    Returns:
        List of created tickets
    """
    # Get email settings
    result = await db.execute(
        select(EmailSettings).where(EmailSettings.workspace_id == workspace_id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        print(f"[Email] No email settings found for workspace {workspace_id}")
        return []
    
    if not settings.incoming_mail_host:
        print(f"[Email] Incoming mail not configured for workspace {workspace_id}")
        return []
    
    # Create service and process emails
    service = EmailToTicketService(settings, workspace_id)
    return await service.process_emails(db)


async def find_ticket_by_reply_for_account(
    db: AsyncSession, 
    workspace_id: int, 
    in_reply_to: str, 
    references: str
) -> Optional[Ticket]:
    """Find ticket from reply headers (In-Reply-To or References) for alternate email accounts"""
    print(f"[DEBUG] find_ticket_by_reply_for_account called with:")
    print(f"[DEBUG]   in_reply_to: '{in_reply_to}'")
    print(f"[DEBUG]   references: '{references}'")
    print(f"[DEBUG]   workspace_id: {workspace_id}")
    
    # Try In-Reply-To first
    if in_reply_to:
        print(f"[DEBUG] Searching processedmail for message_id: '{in_reply_to}'")
        result = await db.execute(
            select(ProcessedMail).where(
                ProcessedMail.message_id == in_reply_to,
                ProcessedMail.workspace_id == workspace_id
            )
        )
        processed = result.scalar_one_or_none()
        print(f"[DEBUG] ProcessedMail result: {processed}")
        if processed and processed.ticket_id:
            print(f"[DEBUG] Found ticket_id: {processed.ticket_id}")
            ticket_result = await db.execute(
                select(Ticket).where(Ticket.id == processed.ticket_id)
            )
            ticket = ticket_result.scalar_one_or_none()
            if ticket and ticket.status in ['closed', 'resolved']:
                print(f"[DEBUG] Found ticket #{ticket.ticket_number} but it's CLOSED - will create new ticket")
                return None
            print(f"[DEBUG] Returning ticket: {ticket.ticket_number if ticket else None}")
            return ticket
    
    # Try References (can contain multiple message IDs)
    if references:
        print(f"[DEBUG] Trying References header")
        ref_ids = references.strip().split()
        print(f"[DEBUG] Parsed reference IDs: {ref_ids}")
        for ref_id in reversed(ref_ids):  # Check from newest to oldest
            ref_id = ref_id.strip()
            print(f"[DEBUG] Checking reference: '{ref_id}'")
            result = await db.execute(
                select(ProcessedMail).where(
                    ProcessedMail.message_id == ref_id,
                    ProcessedMail.workspace_id == workspace_id
                )
            )
            processed = result.scalar_one_or_none()
            if processed and processed.ticket_id:
                ticket_result = await db.execute(
                    select(Ticket).where(Ticket.id == processed.ticket_id)
                )
                ticket = ticket_result.scalar_one_or_none()
                if ticket and ticket.status in ['closed', 'resolved']:
                    print(f"[DEBUG] Found ticket #{ticket.ticket_number} via References but it's CLOSED - will create new ticket")
                    continue  # Try next reference
                print(f"[DEBUG] Found ticket via References: {ticket.ticket_number if ticket else None}")
                return ticket
    
    print(f"[DEBUG] No ticket found via In-Reply-To or References")
    return None


async def find_ticket_by_subject_for_account(db: AsyncSession, workspace_id: int, subject: str) -> Optional[Ticket]:
    """
    Fallback: Find ticket by subject line pattern for alternate email accounts
    Gmail/Outlook include "Re: Ticket #12345" in subject
    """
    import re
    
    print(f"[DEBUG] Trying to find ticket by subject: '{subject}'")
    
    # Clean up the subject - remove Re:, Fwd:, etc.
    clean_subject = re.sub(r'^(Re:|RE:|Fwd:|FWD:|\[.*?\])\s*', '', subject, flags=re.IGNORECASE).strip()
    print(f"[DEBUG] Cleaned subject: '{clean_subject}'")
    
    # Look for patterns like "Ticket #TKT-2025-00042" or "#TKT-2025-00042"
    patterns = [
        r'Ticket\s*#?\s*(TKT-\d{4}-\d+)',  # "Ticket #TKT-2025-00042"
        r'Re:\s*Ticket\s*#?\s*(TKT-\d{4}-\d+)',  # "Re: Ticket #TKT-2025-00042"
        r'#(TKT-\d{4}-\d+)',  # "#TKT-2025-00042"
        r'\[(TKT-\d{4}-\d+)\]',  # "[TKT-2025-00042]"
        r'(TKT-\d{4}-\d{5})',  # Just the ticket number pattern anywhere
    ]
    
    # Try on both original and cleaned subject
    for test_subject in [subject, clean_subject]:
        for pattern in patterns:
            match = re.search(pattern, test_subject, re.IGNORECASE)
            if match:
                ticket_number = match.group(1).upper()
                print(f"[DEBUG] Found potential ticket number in subject: {ticket_number} (pattern: {pattern})")
                
                # Search for ticket by number (exclude closed tickets)
                result = await db.execute(
                    select(Ticket).where(
                        Ticket.ticket_number == ticket_number,
                        Ticket.workspace_id == workspace_id
                    )
                )
                ticket = result.scalar_one_or_none()
                if ticket:
                    # Don't add comments to closed tickets - create new ticket instead
                    if ticket.status in ['closed', 'resolved']:
                        print(f"[DEBUG] Found ticket #{ticket.ticket_number} but it's CLOSED - will create new ticket")
                        return None
                    print(f"[DEBUG] ✅ Found ticket #{ticket.ticket_number} via subject line")
                    return ticket
                else:
                    print(f"[DEBUG] Pattern matched '{ticket_number}' but no ticket found in database")
    
    print(f"[DEBUG] ❌ No ticket number found in subject")
    return None


async def find_ticket_by_sender_for_account(db: AsyncSession, workspace_id: int, sender_email: str) -> Optional[Ticket]:
    """
    Last resort fallback: Find most recent open ticket from this sender
    Only matches if there's exactly ONE open ticket from this email
    """
    print(f"[DEBUG] Trying to find ticket by sender email: '{sender_email}'")
    
    # Search for open tickets from this email (not closed)
    result = await db.execute(
        select(Ticket).where(
            Ticket.guest_email == sender_email,
            Ticket.workspace_id == workspace_id,
            Ticket.status.in_(['new', 'open', 'pending', 'in_progress'])
        ).order_by(Ticket.created_at.desc())
    )
    tickets = result.scalars().all()
    
    if len(tickets) == 1:
        # Only auto-match if there's exactly one open ticket
        print(f"[DEBUG] ✅ Found single open ticket #{tickets[0].ticket_number} from sender")
        return tickets[0]
    elif len(tickets) > 1:
        print(f"[DEBUG] Found {len(tickets)} open tickets from sender - ambiguous, creating new ticket")
    else:
        print(f"[DEBUG] No open tickets found from sender")
    
    return None


async def add_comment_from_email_for_account(
    db: AsyncSession,
    ticket: Ticket,
    sender_name: str,
    sender_email: str,
    body: str
) -> TicketComment:
    """Add a comment to an existing ticket from email reply (for alternate email accounts)"""
    
    # Create comment
    comment = TicketComment(
        ticket_id=ticket.id,
        user_id=None,  # Guest comment from email
        content=f"**Email reply from {sender_name} ({sender_email}):**\n\n{body}",
        is_internal=False,
        created_at=get_local_time()
    )
    db.add(comment)
    
    # Update ticket timestamp
    ticket.updated_at = get_local_time()
    
    # Add history entry
    history = TicketHistory(
        ticket_id=ticket.id,
        user_id=None,
        action='comment_added',
        comment=f'Email reply received from {sender_email}',
        created_at=get_local_time()
    )
    db.add(history)
    
    # Notify all non-admin users in the workspace about email reply
    from app.models.user import User
    
    # Get all non-admin users in the workspace
    users_query = (
        select(User)
        .where(User.workspace_id == ticket.workspace_id)
        .where(User.is_admin == False)
    )
    non_admin_users = (await db.execute(users_query)).scalars().all()
    
    # Create notification for each non-admin user (if they haven't muted)
    for user in non_admin_users:
        # Check if user has muted ticket notifications
        if getattr(user, 'mute_ticket_notifications', False):
            continue
        notification = Notification(
            user_id=user.id,
            type='email_reply',
            message=f'📧 Email reply received on ticket #{ticket.ticket_number} from {sender_email}',
            url=f'/web/tickets/{ticket.id}',
            related_id=ticket.id
        )
        db.add(notification)
    
    await db.commit()
    await db.refresh(comment)
    
    return comment


def _html_to_text_standalone(html: str) -> str:
    """Standalone HTML-to-text converter for use outside the EmailToTicketService class"""
    # Create a temporary service instance to reuse the converter
    service = EmailToTicketService.__new__(EmailToTicketService)
    return service.html_to_text(html)


def _clean_email_body_standalone(body: str) -> str:
    """Standalone email body cleaner for use outside the EmailToTicketService class"""
    service = EmailToTicketService.__new__(EmailToTicketService)
    return service.clean_email_body(body)


async def process_email_account(db: AsyncSession, account) -> List[Ticket]:
    """
    Process emails for an IncomingEmailAccount and create tickets or add comments to existing tickets.
    
    Uses asyncio.to_thread() for blocking IMAP operations to prevent
    blocking the event loop and slowing down the website.
    
    Now supports reply detection via:
    1. In-Reply-To / References headers
    2. Subject line pattern matching (e.g., "Re: Ticket #TKT-2025-00042")
    3. Sender email fallback (single open ticket from same sender)
    
    Args:
        db: Database session
        account: IncomingEmailAccount with IMAP settings
        
    Returns:
        List of created tickets (replies to existing tickets are not included)
    """
    from app.core.database import engine
    from sqlmodel.ext.asyncio.session import AsyncSession as NewAsyncSession
    from app.models.processed_mail import ProcessedMail
    from app.models.notification import Notification
    from app.models.user import User
    
    if not account.imap_host or not account.imap_username:
        return []
    
    # Store account data we need before any async operations
    account_id = account.id
    account_name = account.name
    account_email = account.email_address
    workspace_id = account.workspace_id
    project_id = account.project_id  # Link tickets to this project
    imap_host = account.imap_host
    imap_port = account.imap_port
    imap_username = account.imap_username
    imap_password = account.imap_password
    imap_use_ssl = account.imap_use_ssl
    protocol = getattr(account, 'protocol', 'imap')  # Default to IMAP for backward compatibility
    default_priority = account.default_priority
    default_category = account.default_category
    auto_assign_to_user_id = account.auto_assign_to_user_id
    
    tickets_created = []
    mail = None
    pop3_conn = None
    
    try:
        import imaplib
        import poplib
        import email as email_lib
        from email.header import decode_header
        from email.utils import parseaddr
        
        # Run blocking mail operations in thread pool
        def connect_and_fetch():
            """Synchronous mail connection and fetch (IMAP or POP3)"""
            nonlocal mail, pop3_conn
            
            if protocol == 'pop3':
                # POP3 connection with timeout
                print(f"[Email Account] Using POP3 protocol on {imap_host}:{imap_port}")
                socket.setdefaulttimeout(IMAP_TIMEOUT)
                if imap_use_ssl:
                    pop3_conn = poplib.POP3_SSL(imap_host, imap_port or 995, timeout=IMAP_TIMEOUT)
                else:
                    pop3_conn = poplib.POP3(imap_host, imap_port or 110, timeout=IMAP_TIMEOUT)
                socket.setdefaulttimeout(None)
                
                pop3_conn.user(imap_username)
                pop3_conn.pass_(imap_password)
                
                # Get message count
                num_messages = len(pop3_conn.list()[1])
                print(f"[Email Account] POP3: Found {num_messages} messages")
                
                raw_emails = []
                # Only get last 50 messages to avoid overwhelming
                start_idx = max(1, num_messages - 50 + 1)
                for i in range(start_idx, num_messages + 1):
                    try:
                        response = pop3_conn.retr(i)
                        msg_bytes = b'\r\n'.join(response[1])
                        raw_emails.append({
                            'email_id': str(i).encode(),
                            'msg_bytes': msg_bytes
                        })
                    except Exception as e:
                        print(f"[Email Account] POP3 error fetching message {i}: {e}")
                        continue
                
                return raw_emails
            else:
                # IMAP connection (default) with timeout
                print(f"[Email Account] Using IMAP protocol on {imap_host}:{imap_port}")
                socket.setdefaulttimeout(IMAP_TIMEOUT)
                if imap_use_ssl:
                    mail = imaplib.IMAP4_SSL(imap_host, imap_port or 993, timeout=IMAP_TIMEOUT)
                else:
                    # Non-SSL connection - try STARTTLS for security
                    mail = imaplib.IMAP4(imap_host, imap_port or 143)
                    try:
                        mail.starttls()
                    except Exception:
                        # Server doesn't support STARTTLS, continue without encryption
                        pass
                socket.setdefaulttimeout(None)  # Reset timeout
                
                mail.login(imap_username, imap_password)
                mail.select('INBOX')
                
                # Fetch emails from the last 7 days (not just unread)
                # This ensures we catch emails even if marked as read by phone/webmail
                from datetime import datetime, timedelta
                date_since = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
                status, messages = mail.search(None, f'SINCE {date_since}')
                email_ids = messages[0].split()
                
                print(f"[Email Account] Found {len(email_ids)} messages from last 7 days in INBOX")
                
                raw_emails = []
                for email_id in email_ids:
                    try:
                        status, msg_data = mail.fetch(email_id, '(RFC822)')
                        if msg_data and msg_data[0]:
                            raw_emails.append({
                                'email_id': email_id,
                                'msg_bytes': msg_data[0][1]
                            })
                    except Exception as e:
                        print(f"[Email Account] Error fetching email {email_id}: {e}")
                        continue
                
                return raw_emails
        
        # Fetch emails in thread pool (non-blocking)
        raw_emails = await asyncio.to_thread(connect_and_fetch)
        
        print(f"[Email Account] {account_name}: Found {len(raw_emails)} unread messages to process")
        
        for raw_email in raw_emails:
            email_id = raw_email['email_id']
            try:
                msg = email_lib.message_from_bytes(raw_email['msg_bytes'])
                
                # Get message ID
                message_id = msg.get('Message-ID', f'no-id-{email_id.decode()}')
                
                print(f"[Email Account] Processing email {email_id}: Message-ID={message_id[:50]}...")
                
                # Use a fresh database session for each email to avoid greenlet issues
                async with NewAsyncSession(engine) as fresh_db:
                    # Check if already processed (globally)
                    existing = await fresh_db.execute(
                        select(ProcessedMail).where(ProcessedMail.message_id == message_id)
                    )
                    if existing.scalar_one_or_none():
                        print(f"[Email Account] Email already processed, marking as read")
                        await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                        continue
                    
                    # Extract email info
                    from_header = msg.get('From', '')
                    sender_name, sender_email_addr = parseaddr(from_header)
                    sender_email_addr = sender_email_addr.lower() if sender_email_addr else ''
                    
                    # Decode subject
                    subject_header = msg.get('Subject', 'No Subject')
                    if isinstance(subject_header, bytes):
                        subject = subject_header.decode()
                    else:
                        decoded = decode_header(subject_header)
                        subject = ''
                        for part, charset in decoded:
                            if isinstance(part, bytes):
                                subject += part.decode(charset or 'utf-8', errors='replace')
                            else:
                                subject += part
                    
                    print(f"[Email Account] From: {sender_name} <{sender_email_addr}>")
                    print(f"[Email Account] Subject: {subject}")
                    
                    # Get reply headers for threading detection
                    in_reply_to = msg.get('In-Reply-To', '').strip()
                    references = msg.get('References', '').strip()
                    
                    print(f"[Email Account] In-Reply-To: '{in_reply_to}'")
                    print(f"[Email Account] References: '{references}'")
                    
                    # Extract body (try plain text first, fall back to HTML)
                    body = ''
                    html_body = ''
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain' and not body:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    charset = part.get_content_charset() or 'utf-8'
                                    body = payload.decode(charset, errors='replace')
                            elif content_type == 'text/html' and not html_body:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    charset = part.get_content_charset() or 'utf-8'
                                    html_body = payload.decode(charset, errors='replace')
                    else:
                        content_type = msg.get_content_type()
                        payload = msg.get_payload(decode=True)
                        if payload:
                            charset = msg.get_content_charset() or 'utf-8'
                            decoded = payload.decode(charset, errors='replace')
                            if content_type == 'text/html':
                                html_body = decoded
                            else:
                                body = decoded
                    
                    # If we only have HTML, convert to clean plain text
                    if not body.strip() and html_body:
                        body = _html_to_text_standalone(html_body)
                    
                    # Clean quoted replies from body
                    if body:
                        body = _clean_email_body_standalone(body)
                    
                    # Check if this is a reply to an existing ticket
                    existing_ticket = await find_ticket_by_reply_for_account(
                        fresh_db, workspace_id, in_reply_to, references
                    )
                    
                    # If not found via headers, try by sender email
                    # (Skip subject matching - too aggressive, catches invoice numbers etc.)
                    if not existing_ticket:
                        print(f"[Email Account] Trying sender email fallback...")
                        existing_ticket = await find_ticket_by_sender_for_account(
                            fresh_db, workspace_id, sender_email_addr
                        )
                    
                    if existing_ticket:
                        # Refresh the ticket to ensure all attributes are loaded
                        await fresh_db.refresh(existing_ticket)
                        existing_ticket_id = existing_ticket.id
                        existing_ticket_number = existing_ticket.ticket_number
                        
                        print(f"[Email Account] ✅ MATCH FOUND - Adding comment to ticket #{existing_ticket_number}")
                        
                        # Add as comment to existing ticket
                        await add_comment_from_email_for_account(
                            fresh_db, existing_ticket, sender_name, sender_email_addr, body
                        )
                        
                        # Mark email as processed (linked to existing ticket)
                        processed = ProcessedMail(
                            message_id=message_id,
                            email_from=sender_email_addr or 'unknown@unknown.com',
                            subject=subject,
                            ticket_id=existing_ticket_id,
                            workspace_id=workspace_id
                        )
                        fresh_db.add(processed)
                        await fresh_db.commit()
                        
                        # Mark as read (run in thread)
                        if mail:
                            await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                        
                        print(f"[Email Account] Added comment to ticket #{existing_ticket_number} from {sender_email_addr}")
                        continue  # Move to next email, don't create new ticket
                    
                    print(f"[Email Account] ❌ NO MATCH - Creating new ticket")
                    
                    # Determine priority
                    content = (subject + ' ' + body).lower()
                    urgent_keywords = ['urgent', 'emergency', 'critical', 'asap', 'down', 'not working']
                    high_keywords = ['important', 'high priority', 'soon', 'broken', 'error']
                    
                    if any(keyword in content for keyword in urgent_keywords):
                        priority = 'urgent'
                    elif any(keyword in content for keyword in high_keywords):
                        priority = 'high'
                    else:
                        priority = default_priority
                    
                    # Generate unique ticket number
                    ticket_number = await generate_unique_ticket_number(fresh_db, workspace_id)
                    
                    # Create ticket
                    new_ticket = Ticket(
                        ticket_number=ticket_number,
                        subject=subject[:200],
                        description=body[:5000],
                        priority=priority,
                        status='open',
                        category=default_category,
                        workspace_id=workspace_id,
                        related_project_id=project_id,  # Link to project for this email account
                        created_by_id=None,  # Guest ticket
                        assigned_to_id=auto_assign_to_user_id,  # Auto-assign if configured
                        is_guest=True,
                        guest_name=sender_name.split()[0] if sender_name else "Unknown",
                        guest_surname=sender_name.split()[-1] if sender_name and len(sender_name.split()) > 1 else "",
                        guest_email=sender_email_addr,
                        guest_phone="",
                        guest_company=account_name,  # Use email account name as company
                        guest_branch="",
                        created_at=get_local_time(),
                        updated_at=get_local_time()
                    )
                    
                    fresh_db.add(new_ticket)
                    await fresh_db.commit()
                    await fresh_db.refresh(new_ticket)
                    
                    # Store ID immediately after refresh to avoid lazy loading issues
                    ticket_id = new_ticket.id
                    
                    # Mark email as processed
                    processed = ProcessedMail(
                        message_id=message_id,
                        email_from=sender_email_addr or 'unknown@unknown.com',
                        subject=subject,
                        ticket_id=ticket_id,
                        workspace_id=workspace_id
                    )
                    fresh_db.add(processed)
                    await fresh_db.commit()
                    
                    # Mark as read (run in thread)
                    await asyncio.to_thread(mail.store, email_id, '+FLAGS', '\\Seen')
                    
                    # Notify all admins and users with can_see_all_tickets permission
                    admin_query = select(User).where(
                        User.workspace_id == workspace_id,
                        User.is_active == True,
                        (User.is_admin == True) | (User.can_see_all_tickets == True)
                    )
                    result = await fresh_db.execute(admin_query)
                    notify_users = result.scalars().all()
                    
                    for user in notify_users:
                        # Check if user has muted ticket notifications
                        if getattr(user, 'mute_ticket_notifications', False):
                            continue
                        notification = Notification(
                            user_id=user.id,
                            title=f"📧 New Ticket: #{ticket_number}",
                            message=f"Email from {sender_name} ({sender_email_addr}): {subject[:100]}",
                            type='ticket',
                            url=f'/web/tickets/{ticket_id}',
                            related_id=ticket_id
                        )
                        fresh_db.add(notification)
                    
                    await fresh_db.commit()
                    
                    tickets_created.append(new_ticket)
                    print(f"[Email Account] ✅ Created ticket #{ticket_number} (ID: {ticket_id}) from {sender_email_addr} via {account_name}")
                
            except Exception as e:
                print(f"[Email Account] Error processing email {email_id}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Close connection in thread pool
        if mail:
            await asyncio.to_thread(lambda: (mail.close(), mail.logout()))
        if pop3_conn:
            await asyncio.to_thread(lambda: pop3_conn.quit())
        
    except Exception as e:
        print(f"[Email Account] Error fetching emails for account {account_name}: {e}")
        import traceback
        traceback.print_exc()
        if mail:
            try:
                await asyncio.to_thread(lambda: (mail.close(), mail.logout()))
            except:
                pass
        if pop3_conn:
            try:
                await asyncio.to_thread(lambda: pop3_conn.quit())
            except:
                pass
    
    return tickets_created
