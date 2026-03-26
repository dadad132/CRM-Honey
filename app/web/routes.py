# pyright: reportGeneralTypeIssues=false
# pyright: reportArgumentType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportOperatorIssue=false
# pyright: reportCallIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportMissingImports=false
# pyright: reportAssignmentType=false
# pyright: reportOptionalSubscript=false
# The above directives suppress SQLAlchemy ORM type checker false positives
# SQLAlchemy uses metaprogramming that type checkers don't understand
from __future__ import annotations

from typing import Optional
from pathlib import Path
from datetime import date, datetime, timedelta, time, timezone
import calendar as pycalendar
import os
import uuid
import asyncio
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, Form, HTTPException, Request, File, UploadFile, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import verify_password, get_password_hash
from app.core.email import send_email
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.models.enums import TaskStatus, TaskPriority, MeetingPlatform
from app.models.workspace import Workspace
from app.models.assignment import Assignment
from app.models.comment import Comment
from app.models.comment_attachment import CommentAttachment
from app.models.task_history import TaskHistory
from app.models.notification import Notification
from app.models.chat import Chat, ChatMember, Message
from app.models.meeting import Meeting, MeetingAttendee
from app.models.company import Company
from app.models.contact import Contact
from app.models.lead import Lead
from app.models.deal import Deal
from app.models.activity import Activity

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

# Store original TemplateResponse
_original_template_response = templates.TemplateResponse

def enhanced_template_response(name: str, context: dict, *args, **kwargs):
    """Enhanced TemplateResponse that adds workspace from request state"""
    # ALWAYS add workspace to context if request is present
    if 'request' in context:
        request = context['request']
        # Check if workspace exists in request.state
        if hasattr(request, 'state') and hasattr(request.state, 'workspace'):
            context['workspace'] = request.state.workspace
        # If not in state, try to get it from context (already passed)
        elif 'workspace' not in context:
            context['workspace'] = None
    
    return _original_template_response(name, context, *args, **kwargs)

# Replace the TemplateResponse method - this affects ALL template calls
templates.TemplateResponse = enhanced_template_response

# Convert UTC datetime to local time for display
def utc_to_local(utc_dt):
    """Convert UTC datetime to local time"""
    if utc_dt is None:
        return None
    # Get the local timezone offset
    import time
    if time.daylight:
        offset_seconds = time.altzone
    else:
        offset_seconds = time.timezone
    # Calculate local time
    from datetime import timedelta
    local_dt = utc_dt - timedelta(seconds=offset_seconds)
    return local_dt

# Default timezone for the website - UTC+2 (Africa/Johannesburg)
DEFAULT_TIMEZONE = "Africa/Johannesburg"

def format_datetime_tz(dt, tz_name=None, format_str="%Y-%m-%d %H:%M"):
    """Convert UTC datetime to specified timezone and format it
    
    Note: If tz_name is None, empty, or 'UTC', we use the DEFAULT_TIMEZONE (UTC+2)
    to ensure consistent time display across the website.
    """
    if dt is None:
        return ""
    
    # Always default to Africa/Johannesburg (UTC+2) if no timezone specified or UTC
    if not tz_name or tz_name == "UTC":
        tz_name = DEFAULT_TIMEZONE
    
    # Handle UTC specially to avoid tzdata dependency issues on Windows
    from datetime import timezone as dt_timezone
    
    try:
        from zoneinfo import ZoneInfo
        has_zoneinfo = True
    except ImportError:
        has_zoneinfo = False
    
    try:
        # Try pytz first as it's more reliable on Windows
        import pytz
        if isinstance(dt, datetime):
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=pytz.UTC)
            if tz_name == "UTC":
                target_tz = pytz.UTC
            else:
                target_tz = pytz.timezone(tz_name)
            local_dt = dt.astimezone(target_tz)
            return local_dt.strftime(format_str)
    except ImportError:
        pass
    
    # Fallback to zoneinfo
    if has_zoneinfo:
        try:
            if isinstance(dt, datetime):
                if dt.tzinfo is None:
                    # Use datetime.timezone.utc instead of ZoneInfo("UTC")
                    dt = dt.replace(tzinfo=dt_timezone.utc)
                target_tz = ZoneInfo(tz_name)  # type: ignore[possibly-undefined]
                local_dt = dt.astimezone(target_tz)
                return local_dt.strftime(format_str)
        except Exception:
            pass
    
    # Ultimate fallback - manually apply UTC+2 offset
    if isinstance(dt, datetime):
        try:
            from datetime import timedelta
            # Apply UTC+2 offset manually (Africa/Johannesburg = UTC+2)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=dt_timezone.utc)
            # Create UTC+2 timezone
            utc_plus_2 = dt_timezone(timedelta(hours=2))
            local_dt = dt.astimezone(utc_plus_2)
            return local_dt.strftime(format_str)
        except Exception:
            pass
    
    # Last resort - just format as-is
    return dt.strftime(format_str) if isinstance(dt, datetime) else str(dt)

async def get_workspace_for_user(user_id: int, db: AsyncSession) -> Optional[Workspace]:
    """Get workspace with branding for a user"""
    try:
        user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if not user:
            return None
        workspace = (await db.execute(select(Workspace).where(Workspace.id == user.workspace_id))).scalar_one_or_none()
        return workspace
    except Exception:
        return None

# Add helper functions to Jinja2 globals for use in templates
templates.env.globals['now'] = datetime.utcnow
templates.env.globals['utc_to_local'] = utc_to_local

# Add timezone formatting filter
templates.env.filters['format_datetime_tz'] = format_datetime_tz

router = APIRouter(tags=['web'])


# --------------------------
# Authentication Dependencies
# --------------------------
async def get_current_user(request: Request, db: AsyncSession = Depends(get_session)) -> User:
    """Get current authenticated user or raise HTTPException"""
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user


async def get_current_admin(request: Request, db: AsyncSession = Depends(get_session)) -> User:
    """Get current authenticated admin user or raise HTTPException"""
    user = await get_current_user(request, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# --------------------------
# App Download Page
# --------------------------
@router.get('/download', response_class=HTMLResponse)
async def download_app(request: Request):
    """Download page for mobile app - shows Android APK download or iOS PWA instructions"""
    return templates.TemplateResponse('download.html', {'request': request})


# --------------------------
# Auth (session-based for web)
# --------------------------
@router.get('/login', response_class=HTMLResponse)
async def web_login(request: Request):
    return templates.TemplateResponse('auth/login.html', {'request': request, 'error': None})


@router.post('/login')
async def web_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse('auth/login.html', {'request': request, 'error': 'Invalid username or password'}, status_code=400)
    
    # Check if user is active
    if not user.is_active:
        return templates.TemplateResponse('auth/login.html', {'request': request, 'error': 'Your account has been deactivated. Please contact your administrator.'}, status_code=403)
    
    request.session['user_id'] = user.id
    request.session['workspace_id'] = user.workspace_id
    # Redirect to profile completion if not completed
    if not user.profile_completed:
        return RedirectResponse('/web/profile/complete', status_code=303)
    return RedirectResponse('/web/dashboard', status_code=303)


@router.get('/signup', response_class=HTMLResponse)
async def web_signup(request: Request):
    return templates.TemplateResponse('auth/signup.html', {'request': request, 'error': None})


@router.post('/signup')
async def web_signup_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    company_name: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    # Import validation function
    from app.core.security import validate_password
    
    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return templates.TemplateResponse('auth/signup.html', {'request': request, 'error': error_msg}, status_code=400)
    
    exists = await db.execute(select(User).where(User.username == username))
    if exists.scalar_one_or_none():
        return templates.TemplateResponse('auth/signup.html', {'request': request, 'error': 'Username already taken'}, status_code=400)
    # Create workspace and user
    # Self-registered users become admin of their own workspace
    ws = Workspace(
        name=f"{username}'s Workspace",
        site_title=company_name  # Use company name as the site title
    )
    db.add(ws)
    await db.flush()
    user = User(
        username=username, 
        hashed_password=get_password_hash(password), 
        workspace_id=ws.id,
        profile_completed=False,
        email_verified=True,
        is_admin=True  # Self-registered users are admins of their workspace
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    request.session['user_id'] = user.id
    request.session['workspace_id'] = user.workspace_id
    return RedirectResponse('/web/profile/complete', status_code=303)


@router.post('/logout')
async def web_logout(request: Request):
    request.session.clear()
    return RedirectResponse('/', status_code=303)


# --------------------------
# Profile Completion
# --------------------------
@router.get('/profile/complete', response_class=HTMLResponse)
async def web_profile_complete(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    if user.profile_completed:
        return RedirectResponse('/web/projects', status_code=303)
    return templates.TemplateResponse('auth/profile_complete.html', {'request': request, 'user': user, 'error': None})


@router.post('/profile/complete')
async def web_profile_complete_post(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    preferred_meeting_platform: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    # Check if email is already used by another user
    if email:
        exists = await db.execute(select(User).where(User.email == email, User.id != user_id))
        if exists.scalar_one_or_none():
            return templates.TemplateResponse('auth/profile_complete.html', {'request': request, 'user': user, 'error': 'Email already in use'}, status_code=400)
    user.full_name = full_name
    user.email = email
    if preferred_meeting_platform:
        try:
            user.preferred_meeting_platform = MeetingPlatform(preferred_meeting_platform)
        except ValueError:
            pass
    user.profile_completed = True
    await db.commit()
    return RedirectResponse('/web/projects', status_code=303)


@router.get('/profile', response_class=HTMLResponse)
async def web_profile(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    return templates.TemplateResponse('auth/profile.html', {'request': request, 'user': user})


@router.post('/profile')
async def web_profile_post(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    preferred_meeting_platform: Optional[str] = Form(None),
    calendar_color: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Check if email is already used by another user
    if email:
        exists = await db.execute(select(User).where(User.email == email, User.id != user_id))
        if exists.scalar_one_or_none():
            return templates.TemplateResponse('auth/profile.html', {
                'request': request, 
                'user': user, 
                'error': 'Email already in use'
            }, status_code=400)
    
    user.full_name = full_name
    user.email = email
    if preferred_meeting_platform:
        try:
            user.preferred_meeting_platform = MeetingPlatform(preferred_meeting_platform)
        except ValueError:
            user.preferred_meeting_platform = None
    else:
        user.preferred_meeting_platform = None
    if calendar_color:
        user.calendar_color = calendar_color
    
    
    await db.commit()
    return templates.TemplateResponse('auth/profile.html', {
        'request': request, 
        'user': user, 
        'success': 'Profile updated successfully'
    })


@router.post('/profile/picture')
async def web_profile_picture_upload(
    request: Request,
    profile_picture: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if profile_picture.content_type not in allowed_types:
        return templates.TemplateResponse('auth/profile.html', {
            'request': request,
            'user': user,
            'error': 'Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.'
        }, status_code=400)
    
    # Validate file size (max 5MB)
    content = await profile_picture.read()
    if len(content) > 5 * 1024 * 1024:
        return templates.TemplateResponse('auth/profile.html', {
            'request': request,
            'user': user,
            'error': 'File too large. Maximum size is 5MB.'
        }, status_code=400)
    
    # Create uploads directory if it doesn't exist
    upload_dir = BASE_DIR / 'uploads' / 'profile_pictures'
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Delete old profile picture if it exists
    if user.profile_picture:
        old_file = BASE_DIR / user.profile_picture.lstrip('/')
        if old_file.exists():
            old_file.unlink()
    
    # Generate unique filename
    filename_str = profile_picture.filename or 'upload.jpg'
    file_extension = filename_str.split('.')[-1] if '.' in filename_str else 'jpg'
    filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
    file_path = upload_dir / filename
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Update user profile picture path (relative to BASE_DIR)
    user.profile_picture = f"/uploads/profile_pictures/{filename}"
    await db.commit()
    
    return RedirectResponse('/web/profile?success=picture', status_code=303)


@router.get('/uploads/profile_pictures/{filename}')
async def serve_profile_picture(filename: str):
    """Serve profile picture files"""
    # Prevent path traversal attacks
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = BASE_DIR / 'uploads' / 'profile_pictures' / filename
    
    # Ensure the resolved path is within the uploads directory
    try:
        file_path = file_path.resolve()
        upload_base = (BASE_DIR / 'uploads' / 'profile_pictures').resolve()
        if not str(file_path).startswith(str(upload_base)):
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Profile picture not found")
    return FileResponse(file_path)


# --------------------------
# Google OAuth Integration
# --------------------------
@router.get('/auth/google/link')
async def web_google_oauth_link(request: Request, db: AsyncSession = Depends(get_session)):
    """Initiate Google OAuth flow to link account"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    try:
        from app.core.config import get_settings
        from app.core.google_oauth import get_authorization_url
        
        settings = get_settings()
        
        # Check if Google OAuth is configured
        if not settings.google_client_id or not settings.google_client_secret:
            logger.warning("Google OAuth not configured")
            return RedirectResponse('/web/profile?error=google_config', status_code=303)
        
        logger.info(f"Starting Google OAuth for user {user_id}")
        
        auth_url, state = get_authorization_url(user_id)
        # Store state in session for verification
        request.session['google_oauth_state'] = state
        return RedirectResponse(auth_url, status_code=303)
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {e}", exc_info=True)
        return RedirectResponse('/web/profile?error=google_config', status_code=303)


@router.get('/auth/google/callback')
async def web_google_oauth_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    db: AsyncSession = Depends(get_session)
):
    """Handle Google OAuth callback"""
    if error:
        return RedirectResponse(f'/web/profile?error=google_denied', status_code=303)
    
    if not code or not state:
        return RedirectResponse(f'/web/profile?error=google_invalid', status_code=303)
    
    # Verify state matches session
    session_state = request.session.get('google_oauth_state')
    if not session_state or session_state != state:
        return RedirectResponse(f'/web/profile?error=google_state_mismatch', status_code=303)
    
    try:
        user_id = int(state)
        user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        
        if not user or not user.is_active:
            return RedirectResponse('/web/login', status_code=303)
        
        from app.core.google_oauth import exchange_code_for_tokens, get_google_user_info
        
        # Exchange code for tokens
        token_info = exchange_code_for_tokens(code, state)
        
        # Get user info from Google
        google_user_info = get_google_user_info(token_info['access_token'])
        
        # Update user with Google credentials
        user.google_id = google_user_info.get('id')
        user.google_access_token = token_info['access_token']
        user.google_refresh_token = token_info['refresh_token']
        user.google_token_expiry = token_info['token_expiry']
        
        await db.commit()
        
        # Clear OAuth state from session
        request.session.pop('google_oauth_state', None)
        
        return RedirectResponse('/web/profile?success=google_linked', status_code=303)
        
    except Exception as e:
        logger.error(f"Error in Google OAuth callback: {e}", exc_info=True)
        return RedirectResponse(f'/web/profile?error=google_failed', status_code=303)


@router.post('/auth/google/unlink')
async def web_google_oauth_unlink(request: Request, db: AsyncSession = Depends(get_session)):
    """Unlink Google account"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Clear Google OAuth fields
    user.google_id = None
    user.google_access_token = None
    user.google_refresh_token = None
    user.google_token_expiry = None
    
    await db.commit()
    
    return RedirectResponse('/web/profile?success=google_unlinked', status_code=303)


# --------------------------
# Dashboard
# --------------------------
@router.get('/dashboard', response_class=HTMLResponse)
async def web_dashboard(request: Request, view: Optional[str] = None, user_id: Optional[int] = None, db: AsyncSession = Depends(get_session)):
    """Main dashboard with stats and overview"""
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can see user view
    if view == 'user' and not user.is_admin:
        view = 'personal'
    
    from app.models.project_member import ProjectMember
    from datetime import timedelta
    from sqlalchemy import func
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Get user's projects (admin sees all, user sees assigned)
    if user.is_admin:
        projects_result = await db.execute(
            select(Project)
            .where(Project.workspace_id == user.workspace_id, Project.is_archived == False)
        )
        projects = projects_result.scalars().all()
        project_ids = [p.id for p in projects]
    else:
        member_result = await db.execute(
            select(ProjectMember.project_id)
            .where(ProjectMember.user_id == current_user_id)
        )
        project_ids = [r[0] for r in member_result.fetchall()]
        projects_result = await db.execute(
            select(Project)
            .where(Project.id.in_(project_ids), Project.is_archived == False)
        )
        projects = projects_result.scalars().all()
    
    # My Tasks stats
    my_tasks_result = await db.execute(
        select(Task)
        .join(Assignment, Task.id == Assignment.task_id)
        .where(Assignment.assignee_id == current_user_id, Task.status != TaskStatus.done)
    )
    my_tasks = my_tasks_result.scalars().all()
    
    # Tasks done this week
    my_done_result = await db.execute(
        select(func.count())
        .select_from(Task)
        .join(Assignment, Task.id == Assignment.task_id)
        .where(
            Assignment.assignee_id == current_user_id,
            Task.status == TaskStatus.done,
            Task.updated_at >= datetime.combine(week_ago, time.min)
        )
    )
    my_tasks_done = my_done_result.scalar() or 0
    
    # Tasks due soon (next 7 days)
    tasks_due_result = await db.execute(
        select(Task, Project.name.label('project_name'))
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Task.id == Assignment.task_id)
        .where(
            Assignment.assignee_id == current_user_id,
            Task.status != TaskStatus.done,
            Task.due_date.isnot(None),
            Task.due_date <= today + timedelta(days=7)
        )
        .order_by(Task.due_date)
    )
    tasks_due_rows = tasks_due_result.fetchall()
    tasks_due_soon = []
    for row in tasks_due_rows:
        task = row[0]
        # Create a dict-like object to add project_name
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "project_id": task.project_id,
            "project_name": row[1]
        }
        tasks_due_soon.append(task_dict)
    
    # Tickets removed
    open_tickets = []
    urgent_tickets = 0
    high_tickets = 0
    
    # Meetings today
    meetings_result = await db.execute(
        select(func.count())
        .select_from(Meeting)
        .join(MeetingAttendee, Meeting.id == MeetingAttendee.meeting_id)
        .where(
            MeetingAttendee.user_id == current_user_id,
            Meeting.date == today,
            Meeting.is_cancelled == False
        )
    )
    meetings_today = meetings_result.scalar() or 0
    
    # Upcoming meetings (next 7 days)
    upcoming_result = await db.execute(
        select(Meeting)
        .join(MeetingAttendee, Meeting.id == MeetingAttendee.meeting_id)
        .where(
            MeetingAttendee.user_id == current_user_id,
            Meeting.date >= today,
            Meeting.date <= today + timedelta(days=7),
            Meeting.is_cancelled == False
        )
        .order_by(Meeting.date, Meeting.start_time)
        .limit(5)
    )
    upcoming_meetings = upcoming_result.scalars().all()
    
    # Team members count
    team_result = await db.execute(
        select(func.count())
        .select_from(User)
        .where(User.workspace_id == user.workspace_id, User.is_active == True)
    )
    total_team_members = team_result.scalar() or 0
    
    # ========== ENHANCED RECENT ACTIVITY ==========
    from app.models.task_history import TaskHistory
    
    # 1. User's recent activities (what the user did)
    my_activities_result = await db.execute(
        select(TaskHistory, Task.title.label('task_title'), Project.name.label('project_name'))
        .join(Task, TaskHistory.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(
            TaskHistory.editor_id == current_user_id,
            Task.project_id.in_(project_ids) if project_ids else True
        )
        .order_by(TaskHistory.created_at.desc())
        .limit(10)
    )
    my_activities_raw = my_activities_result.fetchall()
    
    recent_activities = []
    for activity, task_title, project_name in my_activities_raw:
        activity_type = 'task_created' if activity.field == 'created' else 'task_updated'
        if activity.field == 'status' and activity.new_value == 'done':
            activity_type = 'task_completed'
        
        # Create a readable description
        if activity.field == 'created':
            desc = f"You created task: {task_title}"
        elif activity.field == 'status':
            desc = f"You changed status to {activity.new_value} on: {task_title}"
        elif activity.field == 'assigned':
            desc = f"You assigned task: {task_title}"
        else:
            desc = f"You updated {activity.field.replace('_', ' ')} on: {task_title}"
        
        recent_activities.append({
            'type': activity_type,
            'description': desc,
            'task_id': activity.task_id,
            'task_title': task_title,
            'project_name': project_name,
            'created_at': activity.created_at
        })
    
    # 2. Tasks allocated TO the user (by others)
    tasks_allocated_to_me_result = await db.execute(
        select(Task, Project.name.label('project_name'), User.full_name.label('creator_name'), User.username.label('creator_username'))
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Task.id == Assignment.task_id)
        .join(User, Task.creator_id == User.id)
        .where(
            Assignment.assignee_id == current_user_id,
            Task.creator_id != current_user_id,  # Not created by me
            Task.status != TaskStatus.done,
            Project.workspace_id == user.workspace_id
        )
        .order_by(Task.created_at.desc())
        .limit(5)
    )
    tasks_allocated_to_me = []
    for task, project_name, creator_name, creator_username in tasks_allocated_to_me_result.fetchall():
        tasks_allocated_to_me.append({
            'id': task.id,
            'title': task.title,
            'project_name': project_name,
            'creator': creator_name or creator_username,
            'due_date': task.due_date,
            'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
            'status': task.status.value if hasattr(task.status, 'value') else task.status,
            'created_at': task.created_at
        })
    
    # 3. Tasks the user allocated to OTHERS
    tasks_allocated_by_me_result = await db.execute(
        select(Task, Project.name.label('project_name'), User.full_name.label('assignee_name'), User.username.label('assignee_username'))
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Task.id == Assignment.task_id)
        .join(User, Assignment.assignee_id == User.id)
        .where(
            Task.creator_id == current_user_id,
            Assignment.assignee_id != current_user_id,  # Assigned to someone else
            Task.status != TaskStatus.done,
            Project.workspace_id == user.workspace_id
        )
        .order_by(Task.created_at.desc())
        .limit(5)
    )
    tasks_allocated_by_me = []
    for task, project_name, assignee_name, assignee_username in tasks_allocated_by_me_result.fetchall():
        tasks_allocated_by_me.append({
            'id': task.id,
            'title': task.title,
            'project_name': project_name,
            'assignee': assignee_name or assignee_username,
            'due_date': task.due_date,
            'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
            'status': task.status.value if hasattr(task.status, 'value') else task.status,
            'created_at': task.created_at
        })
    
    # 4. Overdue tasks assigned to this user
    overdue_tasks_result = await db.execute(
        select(Task, Project.name.label('project_name'))
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Task.id == Assignment.task_id)
        .where(
            Assignment.assignee_id == current_user_id,
            Task.status != TaskStatus.done,
            Task.due_date < today,
            Project.workspace_id == user.workspace_id
        )
        .order_by(Task.due_date.asc())
        .limit(20)
    )
    overdue_tasks = []
    for task, project_name in overdue_tasks_result.fetchall():
        days_overdue = (today - task.due_date).days
        overdue_tasks.append({
            'id': task.id,
            'title': task.title,
            'project_name': project_name,
            'due_date': task.due_date,
            'days_overdue': days_overdue,
            'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
            'status': task.status.value if hasattr(task.status, 'value') else task.status
        })
    
    # 5. Task progress updates (what others did on tasks related to user)
    # Get tasks assigned to user or created by user
    my_related_tasks = await db.execute(
        select(Task.id)
        .join(Assignment, Task.id == Assignment.task_id, isouter=True)
        .where(
            or_(
                Assignment.assignee_id == current_user_id,
                Task.creator_id == current_user_id
            )
        )
    )
    my_task_ids = [r[0] for r in my_related_tasks.fetchall()]
    
    task_progress_updates = []
    if my_task_ids:
        progress_result = await db.execute(
            select(TaskHistory, Task.title.label('task_title'), User.full_name.label('user_name'), User.username.label('user_username'))
            .join(Task, TaskHistory.task_id == Task.id)
            .join(User, TaskHistory.editor_id == User.id)
            .where(
                TaskHistory.task_id.in_(my_task_ids),
                TaskHistory.editor_id != current_user_id,  # Done by others
                TaskHistory.created_at >= datetime.combine(week_ago, time.min)
            )
            .order_by(TaskHistory.created_at.desc())
            .limit(10)
        )
        
        for history, task_title, user_name, user_username in progress_result.fetchall():
            user_display = user_name or user_username
            if history.field == 'status':
                desc = f"{user_display} changed status to {history.new_value}"
            elif history.field == 'comment':
                desc = f"{user_display} added a comment"
            else:
                desc = f"{user_display} updated {history.field.replace('_', ' ')}"
            
            task_progress_updates.append({
                'task_id': history.task_id,
                'task_title': task_title,
                'description': desc,
                'user_name': user_display,
                'action': history.field,
                'new_value': history.new_value,
                'created_at': history.created_at
            })
    
    # Admin stats - team performance
    team_tasks_completed = 0
    avg_response_time = None
    team_members = []
    selected_user = None
    selected_user_stats = {}
    selected_user_tasks = []
    selected_user_projects = []
    
    if user.is_admin:
        # Tasks completed by team this week
        team_done_result = await db.execute(
            select(func.count())
            .select_from(Task)
            .where(
                Task.project_id.in_(project_ids) if project_ids else True,
                Task.status == TaskStatus.done,
                Task.updated_at >= datetime.combine(week_ago, time.min)
            )
        )
        team_tasks_completed = team_done_result.scalar() or 0
        
        team_tickets_resolved = 0
        
        # User view - get all team members for selector
        if view == 'user':
            # Get all team members for the selector
            team_members_result = await db.execute(
                select(User)
                .where(User.workspace_id == user.workspace_id, User.is_active == True)
                .order_by(User.full_name)
            )
            team_members = team_members_result.scalars().all()
            
            # If a specific user_id is selected, get their data
            if user_id:
                selected_user_result = await db.execute(
                    select(User).where(User.id == user_id, User.workspace_id == user.workspace_id)
                )
                selected_user = selected_user_result.scalar_one_or_none()
                
                if selected_user:
                    # Get selected user's open tasks
                    su_tasks_result = await db.execute(
                        select(func.count())
                        .select_from(Task)
                        .join(Assignment, Task.id == Assignment.task_id)
                        .where(Assignment.assignee_id == user_id, Task.status != TaskStatus.done)
                    )
                    su_open_tasks = su_tasks_result.scalar() or 0
                    
                    # Get selected user's done tasks this week
                    su_done_result = await db.execute(
                        select(func.count())
                        .select_from(Task)
                        .join(Assignment, Task.id == Assignment.task_id)
                        .where(
                            Assignment.assignee_id == user_id,
                            Task.status == TaskStatus.done,
                            Task.updated_at >= datetime.combine(week_ago, time.min)
                        )
                    )
                    su_done_tasks = su_done_result.scalar() or 0
                    
                    su_open_tickets = 0
                    
                    # Get selected user's overdue tasks
                    su_overdue_result = await db.execute(
                        select(func.count())
                        .select_from(Task)
                        .join(Assignment, Task.id == Assignment.task_id)
                        .where(
                            Assignment.assignee_id == user_id,
                            Task.status != TaskStatus.done,
                            Task.due_date < today
                        )
                    )
                    su_overdue_tasks = su_overdue_result.scalar() or 0
                    
                    # Get selected user's projects
                    su_projects_result = await db.execute(
                        select(Project)
                        .join(ProjectMember, Project.id == ProjectMember.project_id)
                        .where(ProjectMember.user_id == user_id, Project.is_archived == False)
                    )
                    selected_user_projects = su_projects_result.scalars().all()
                    
                    selected_user_stats = {
                        'open_tasks': su_open_tasks,
                        'done_this_week': su_done_tasks,
                        'open_tickets': su_open_tickets,
                        'overdue_tasks': su_overdue_tasks,
                        'projects': len(selected_user_projects)
                    }
                    
                    # Get selected user's tasks due soon
                    su_tasks_due_result = await db.execute(
                        select(Task, Project.name.label('project_name'))
                        .join(Project, Task.project_id == Project.id)
                        .join(Assignment, Task.id == Assignment.task_id)
                        .where(
                            Assignment.assignee_id == user_id,
                            Task.status != TaskStatus.done,
                            Task.due_date.isnot(None),
                            Task.due_date <= today + timedelta(days=14)
                        )
                        .order_by(Task.due_date)
                        .limit(10)
                    )
                    su_tasks_rows = su_tasks_due_result.fetchall()
                    for row in su_tasks_rows:
                        task = row[0]
                        selected_user_tasks.append({
                            "id": task.id,
                            "title": task.title,
                            "status": task.status,
                            "priority": task.priority,
                            "due_date": task.due_date,
                            "project_name": row[1]
                        })
    
    stats = {
        'my_tasks': len(my_tasks),
        'my_tasks_done': my_tasks_done,
        'open_tickets': len(open_tickets),
        'urgent_tickets': urgent_tickets,
        'high_tickets': high_tickets,
        'active_projects': len(projects),
        'total_team_members': total_team_members,
        'meetings_today': meetings_today,
        'team_tasks_completed': team_tasks_completed,
        'team_tickets_resolved': team_tickets_resolved,
        'avg_response_time': avg_response_time
    }
    
    workspace = await get_workspace_for_user(current_user_id, db)
    
    return templates.TemplateResponse('dashboard/index.html', {
        'request': request,
        'user': user,
        'stats': stats,
        'tasks_due_soon': tasks_due_soon,
        'upcoming_meetings': upcoming_meetings,
        'recent_activities': recent_activities,
        'tasks_allocated_to_me': tasks_allocated_to_me,
        'tasks_allocated_by_me': tasks_allocated_by_me,
        'overdue_tasks': overdue_tasks,
        'task_progress_updates': task_progress_updates,
        'projects': projects,
        'today': today,
        'workspace': workspace,
        'view': view or 'personal',
        'team_members': team_members,
        'selected_user': selected_user,
        'selected_user_stats': selected_user_stats,
        'selected_user_tasks': selected_user_tasks,
        'selected_user_projects': selected_user_projects
    })


@router.post('/dashboard/quick-task')
async def web_dashboard_quick_task(
    request: Request,
    title: str = Form(...),
    project_id: int = Form(...),
    priority: str = Form('medium'),
    due_date: Optional[date] = Form(None),
    customer_name: Optional[str] = Form(None),
    customer_surname: Optional[str] = Form(None),
    customer_email: Optional[str] = Form(None),
    customer_phone: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    """Quick add task from dashboard"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify project exists and user has access
    project = (await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not project:
        return RedirectResponse('/web/dashboard?error=invalid_project', status_code=303)
    
    # Create task
    task = Task(
        title=title,
        project_id=project_id,
        creator_id=user_id,
        priority=TaskPriority(priority),
        due_date=due_date,
        customer_name=customer_name or None,
        customer_surname=customer_surname or None,
        customer_email=customer_email or None,
        customer_phone=customer_phone or None
    )
    db.add(task)
    await db.flush()
    
    # Auto-assign to creator
    assignment = Assignment(task_id=task.id, assignee_id=user_id)
    db.add(assignment)
    
    # Add task history
    history = TaskHistory(
        task_id=task.id,
        editor_id=user_id,
        field='created',
        new_value=title
    )
    db.add(history)
    
    await db.commit()
    
    return RedirectResponse('/web/dashboard', status_code=303)


# --------------------------
# What Changed While You Were Away - AI Summary Feature
# --------------------------
@router.get('/dashboard/what-changed')
async def get_what_changed(request: Request, db: AsyncSession = Depends(get_session)):
    """Get summary of changes since user's last visit"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'error': 'User not found'}, status_code=404)
    
    from app.models.task_history import TaskHistory
    from app.models.project_member import ProjectMember
    from datetime import timedelta
    
    # Determine the time range to check
    now = datetime.utcnow()
    last_seen = user.last_seen_at or (now - timedelta(hours=24))  # Default to 24 hours if never tracked
    time_away = now - last_seen
    
    # Only show if away for more than 30 minutes
    if time_away < timedelta(minutes=30):
        return JSONResponse({
            'show_summary': False,
            'reason': 'Not away long enough',
            'minutes_away': int(time_away.total_seconds() / 60)
        })
    
    # Get user's projects
    if user.is_admin:
        projects_result = await db.execute(
            select(Project.id)
            .where(Project.workspace_id == user.workspace_id, Project.is_archived == False)
        )
        project_ids = [r[0] for r in projects_result.fetchall()]
    else:
        member_result = await db.execute(
            select(ProjectMember.project_id)
            .where(ProjectMember.user_id == user_id)
        )
        project_ids = [r[0] for r in member_result.fetchall()]
    
    changes = {
        'time_away_hours': round(time_away.total_seconds() / 3600, 1),
        'time_away_display': format_time_away(time_away),
        'last_seen': last_seen.isoformat() if last_seen else None,
        'preference': user.away_summary_preference or 'ask',
        'new_tasks_assigned': [],
        'task_updates': [],
        'new_tickets': [],
        'ticket_updates': [],
        'completed_tasks': [],
        'meetings_scheduled': [],
        'summary': ''
    }
    
    # 1. New tasks assigned to user since last seen
    new_tasks_result = await db.execute(
        select(Task, Project.name.label('project_name'), User.full_name.label('creator_name'))
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Task.id == Assignment.task_id)
        .join(User, Task.creator_id == User.id)
        .where(
            Assignment.assignee_id == user_id,
            Task.created_at > last_seen,
            Task.creator_id != user_id  # Not self-assigned
        )
        .order_by(Task.created_at.desc())
    )
    for task, project_name, creator_name in new_tasks_result.fetchall():
        changes['new_tasks_assigned'].append({
            'id': task.id,
            'title': task.title,
            'project': project_name,
            'creator': creator_name or 'Unknown',
            'priority': task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
            'due_date': task.due_date.isoformat() if task.due_date else None
        })
    
    # 2. Updates on tasks assigned to user or created by user
    my_task_ids_result = await db.execute(
        select(Task.id)
        .join(Assignment, Task.id == Assignment.task_id, isouter=True)
        .where(
            or_(Assignment.assignee_id == user_id, Task.creator_id == user_id)
        )
    )
    my_task_ids = [r[0] for r in my_task_ids_result.fetchall()]
    
    if my_task_ids:
        task_updates_result = await db.execute(
            select(TaskHistory, Task.title.label('task_title'), User.full_name.label('editor_name'))
            .join(Task, TaskHistory.task_id == Task.id)
            .join(User, TaskHistory.editor_id == User.id)
            .where(
                TaskHistory.task_id.in_(my_task_ids),
                TaskHistory.created_at > last_seen,
                TaskHistory.editor_id != user_id  # Changes by others
            )
            .order_by(TaskHistory.created_at.desc())
            .limit(20)
        )
        for history, task_title, editor_name in task_updates_result.fetchall():
            if history.field == 'status' and history.new_value == 'done':
                changes['completed_tasks'].append({
                    'task_id': history.task_id,
                    'title': task_title,
                    'completed_by': editor_name or 'Unknown'
                })
            else:
                changes['task_updates'].append({
                    'task_id': history.task_id,
                    'title': task_title,
                    'field': history.field,
                    'new_value': history.new_value,
                    'editor': editor_name or 'Unknown'
                })
    

    

    
    # 5. Meetings scheduled during absence
    meetings_result = await db.execute(
        select(Meeting)
        .join(MeetingAttendee, Meeting.id == MeetingAttendee.meeting_id)
        .where(
            MeetingAttendee.user_id == user_id,
            Meeting.created_at > last_seen,
            Meeting.is_cancelled == False
        )
        .order_by(Meeting.date, Meeting.start_time)
    )
    for meeting in meetings_result.scalars().all():
        changes['meetings_scheduled'].append({
            'id': meeting.id,
            'title': meeting.title,
            'date': meeting.date.isoformat() if meeting.date else None,
            'time': meeting.start_time.strftime('%H:%M') if meeting.start_time else None
        })
    
    # Generate AI-like summary
    changes['summary'] = generate_away_summary(changes)
    
    # Determine if we should show the summary
    total_changes = (
        len(changes['new_tasks_assigned']) + 
        len(changes['task_updates']) + 
        len(changes['new_tickets']) + 
        len(changes['completed_tasks']) +
        len(changes['meetings_scheduled'])
    )
    
    changes['show_summary'] = total_changes > 0
    changes['total_changes'] = total_changes
    
    return JSONResponse(changes)


@router.post('/dashboard/update-last-seen')
async def update_last_seen(request: Request, db: AsyncSession = Depends(get_session)):
    """Update user's last seen timestamp"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user:
        user.last_seen_at = datetime.utcnow()
        await db.commit()
    
    return JSONResponse({'success': True})


@router.post('/dashboard/away-preference')
async def update_away_preference(request: Request, db: AsyncSession = Depends(get_session)):
    """Update user's preference for away summary"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    data = await request.json()
    preference = data.get('preference', 'ask')
    
    if preference not in ['always', 'ask', 'never']:
        return JSONResponse({'error': 'Invalid preference'}, status_code=400)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user:
        user.away_summary_preference = preference
        await db.commit()
    
    return JSONResponse({'success': True, 'preference': preference})


def format_time_away(delta: timedelta) -> str:
    """Format time away into human-readable string"""
    total_seconds = int(delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours >= 24:
        days = hours // 24
        remaining_hours = hours % 24
        if days == 1:
            return f"1 day and {remaining_hours} hours" if remaining_hours else "1 day"
        return f"{days} days and {remaining_hours} hours" if remaining_hours else f"{days} days"
    elif hours > 0:
        if hours == 1:
            return f"1 hour and {minutes} minutes" if minutes else "1 hour"
        return f"{hours} hours and {minutes} minutes" if minutes else f"{hours} hours"
    else:
        return f"{minutes} minutes"


def generate_away_summary(changes: dict) -> str:
    """Generate a friendly AI-style summary of changes"""
    parts = []
    
    time_away = changes.get('time_away_display', 'a while')
    
    # New tasks assigned
    new_tasks = len(changes.get('new_tasks_assigned', []))
    if new_tasks > 0:
        if new_tasks == 1:
            task = changes['new_tasks_assigned'][0]
            parts.append(f"📋 **{task['creator']}** assigned you a new task: \"{task['title']}\"")
        else:
            parts.append(f"📋 You have **{new_tasks} new tasks** assigned to you")
    
    # Completed tasks
    completed = len(changes.get('completed_tasks', []))
    if completed > 0:
        if completed == 1:
            task = changes['completed_tasks'][0]
            parts.append(f"✅ **{task['completed_by']}** completed the task: \"{task['title']}\"")
        else:
            parts.append(f"✅ **{completed} tasks** were completed by your team")
    
    # Task updates
    updates = len(changes.get('task_updates', []))
    if updates > 0:
        parts.append(f"📝 **{updates} updates** were made on tasks you're involved with")
    

    
    # Meetings
    meetings = len(changes.get('meetings_scheduled', []))
    if meetings > 0:
        if meetings == 1:
            meeting = changes['meetings_scheduled'][0]
            parts.append(f"📅 **1 meeting** was scheduled: \"{meeting['title']}\"")
        else:
            parts.append(f"📅 **{meetings} meetings** were scheduled for you")
    
    if not parts:
        return f"🎉 All caught up! Nothing significant happened while you were away."
    
    intro = f"Welcome back! Here's what happened in the last **{time_away}**:\n\n"
    return intro + "\n\n".join(parts)


# --------------------------
# Email Verification (kept for later, not enforced)
# --------------------------
@router.get('/verify-email', response_class=HTMLResponse)
async def web_verify_email(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    return templates.TemplateResponse('auth/verify_email.html', {'request': request, 'user': user, 'error': None, 'sent': False})


@router.post('/verify-email/request')
async def web_verify_email_request(request: Request, db: AsyncSession = Depends(get_session)):
    # No-op while OTP disabled
    return templates.TemplateResponse('auth/verify_email.html', {'request': request, 'user': None, 'error': None, 'sent': True})


@router.post('/verify-email/confirm')
async def web_verify_email_confirm(request: Request, code: str = Form(...), db: AsyncSession = Depends(get_session)):
    # No-op while OTP disabled
    return RedirectResponse('/web/projects', status_code=303)


# --------------------------
# Global Search
# --------------------------
# TODO: FUTURE FEATURE - Add Attachment Search
# Currently searches: Tasks, Projects
# Need to add search for attachments:
#   - TaskAttachment (search by filename, and future 'label' field)
#   - CommentAttachment (search by filename, and future 'label' field)
# Implementation:
#   1. Add 'attachments' to results dict
#   2. Query all attachment tables where filename.ilike(search_term) OR label.ilike(search_term)
#   3. Join with parent entity (Task/Comment) to get context
#   4. Return: filename, label, parent_type (task/comment), parent_id, parent_title
#   5. Update search/results.html template to display attachment results
#   6. Link attachments to their parent entity detail page
@router.get('/search')
async def web_global_search(
    request: Request,
    q: str = '',
    db: AsyncSession = Depends(get_session)
):
    """Global search across tasks, projects, and comments"""
    
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    results = {
        'tasks': [],
        'projects': [],
        'comments': [],
        'query': q
    }
    
    if q and len(q) >= 2:
        search_term = f'%{q}%'
        
        # Search tasks
        task_results = await db.execute(
            select(Task, Project.name.label('project_name'))
            .join(Project, Task.project_id == Project.id)
            .where(
                Project.workspace_id == user.workspace_id,
                Task.is_archived == False,
                (Task.title.ilike(search_term) | Task.description.ilike(search_term))
            )
            .limit(10)
        )
        for row in task_results.fetchall():
            task = row[0]
            results['tasks'].append({
                'id': task.id,
                'title': task.title,
                'project_name': row[1],
                'status': task.status.value if hasattr(task.status, 'value') else task.status,
                'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority
            })
        
        # Search projects
        project_results = await db.execute(
            select(Project)
            .where(
                Project.workspace_id == user.workspace_id,
                Project.is_archived == False,
                (Project.name.ilike(search_term) | Project.description.ilike(search_term))
            )
            .limit(10)
        )
        for project in project_results.scalars().all():
            results['projects'].append({
                'id': project.id,
                'name': project.name,
                'description': project.description[:100] if project.description else None
            })
        
        # Search comments
        comment_results = await db.execute(
            select(Comment, Task.id.label('task_id'), Task.title.label('task_title'), 
                   Project.name.label('project_name'), User.full_name.label('author_name'))
            .join(Task, Comment.task_id == Task.id)
            .join(Project, Task.project_id == Project.id)
            .join(User, Comment.author_id == User.id)
            .where(
                Project.workspace_id == user.workspace_id,
                Comment.content.ilike(search_term)
            )
            .order_by(Comment.created_at.desc())
            .limit(10)
        )
        for row in comment_results.fetchall():
            comment = row[0]
            results['comments'].append({
                'id': comment.id,
                'content': comment.content[:200] + '...' if len(comment.content) > 200 else comment.content,
                'task_id': row[1],
                'task_title': row[2],
                'project_name': row[3],
                'author_name': row[4],
                'created_at': comment.created_at
            })
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JSONResponse(results)
    
    return templates.TemplateResponse('search/results.html', {
        'request': request,
        'user': user,
        'results': results,
        'query': q
    })


@router.get('/api/search')
async def api_global_search(
    request: Request,
    q: str = '',
    db: AsyncSession = Depends(get_session)
):
    """API endpoint for global search (used by search modal)"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'tasks': [], 'projects': [], 'comments': []})
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'tasks': [], 'projects': [], 'comments': []})
    
    results = {'tasks': [], 'projects': [], 'comments': []}
    
    if q and len(q) >= 2:
        search_term = f'%{q}%'
        
        # Search tasks
        task_results = await db.execute(
            select(Task, Project.name.label('project_name'))
            .join(Project, Task.project_id == Project.id)
            .where(
                Project.workspace_id == user.workspace_id,
                Task.is_archived == False,
                (Task.title.ilike(search_term) | Task.description.ilike(search_term))
            )
            .limit(5)
        )
        for row in task_results.fetchall():
            task = row[0]
            results['tasks'].append({
                'id': task.id,
                'title': task.title,
                'project_name': row[1],
                'url': f'/web/tasks/{task.id}'
            })
        
        # Search projects
        project_results = await db.execute(
            select(Project)
            .where(
                Project.workspace_id == user.workspace_id,
                Project.is_archived == False,
                Project.name.ilike(search_term)
            )
            .limit(5)
        )
        for project in project_results.scalars().all():
            results['projects'].append({
                'id': project.id,
                'name': project.name,
                'url': f'/web/projects/{project.id}'
            })
        
        # Search comments
        comment_results = await db.execute(
            select(Comment, Task.id.label('task_id'), Task.title.label('task_title'))
            .join(Task, Comment.task_id == Task.id)
            .join(Project, Task.project_id == Project.id)
            .where(
                Project.workspace_id == user.workspace_id,
                Comment.content.ilike(search_term)
            )
            .order_by(Comment.created_at.desc())
            .limit(5)
        )
        for row in comment_results.fetchall():
            comment = row[0]
            results['comments'].append({
                'id': comment.id,
                'content': comment.content[:100] + '...' if len(comment.content) > 100 else comment.content,
                'task_id': row[1],
                'task_title': row[2],
                'url': f'/web/tasks/{row[1]}'
            })
    
    return JSONResponse(results)


# --------------------------
# Task Duplication
# --------------------------
@router.post('/tasks/{task_id}/duplicate')
async def web_task_duplicate(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Duplicate a task with all its details"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get original task
    original = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not original:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Create duplicate
    new_task = Task(
        title=f"Copy of {original.title}",
        description=original.description,
        project_id=original.project_id,
        creator_id=user_id,
        status=TaskStatus.todo,
        priority=original.priority,
        due_date=original.due_date,
        due_time=original.due_time,
        start_date=original.start_date,
        start_time=original.start_time,
        estimated_hours=original.estimated_hours,
        working_days=original.working_days
    )
    db.add(new_task)
    await db.flush()
    
    # Copy assignments
    assignments = (await db.execute(
        select(Assignment).where(Assignment.task_id == task_id)
    )).scalars().all()
    
    for orig_assign in assignments:
        new_assign = Assignment(
            task_id=new_task.id,
            assignee_id=orig_assign.assignee_id
        )
        db.add(new_assign)
    
    # Copy subtasks
    from app.models.subtask import Subtask
    subtasks = (await db.execute(
        select(Subtask).where(Subtask.task_id == task_id)
    )).scalars().all()
    
    for orig_subtask in subtasks:
        new_subtask = Subtask(
            task_id=new_task.id,
            title=orig_subtask.title,
            is_completed=False,
            order=orig_subtask.order
        )
        db.add(new_subtask)
    
    # Add history
    history = TaskHistory(
        task_id=new_task.id,
        editor_id=user_id,
        field='created',
        new_value=f"Duplicated from task #{task_id}"
    )
    db.add(history)
    
    await db.commit()
    
    return RedirectResponse(f'/web/tasks/{new_task.id}', status_code=303)


# --------------------------
# Time Tracking
# --------------------------
@router.post('/tasks/{task_id}/time-log')
async def web_task_add_time_log(
    request: Request,
    task_id: int,
    hours: float = Form(...),
    description: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    """Log time spent on a task"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists
    task = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Create time log
    from app.models.task_extensions import TimeLog
    time_log = TimeLog(
        task_id=task_id,
        user_id=user_id,
        hours=hours,
        description=description
    )
    db.add(time_log)
    
    await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.get('/tasks/{task_id}/time-logs')
async def web_task_get_time_logs(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Get time logs for a task"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'logs': [], 'total_hours': 0})
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'logs': [], 'total_hours': 0})
    
    # Verify task exists
    task = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not task:
        return JSONResponse({'logs': [], 'total_hours': 0})
    
    # Get time logs
    from app.models.task_extensions import TimeLog
    logs_result = await db.execute(
        select(TimeLog, User.full_name, User.username)
        .join(User, TimeLog.user_id == User.id)
        .where(TimeLog.task_id == task_id)
        .order_by(TimeLog.logged_at.desc())
    )
    
    logs = []
    total_hours = 0
    for row in logs_result.fetchall():
        log = row[0]
        logs.append({
            'id': log.id,
            'hours': log.hours,
            'description': log.description,
            'user_name': row[1] or row[2],
            'logged_at': log.logged_at.isoformat() if log.logged_at else None
        })
        total_hours += log.hours
    
    return JSONResponse({'logs': logs, 'total_hours': total_hours})


# --------------------------
# Notifications (minimal for layout)
# --------------------------
@router.get('/notifications/count', response_class=HTMLResponse)
async def web_notifications_count(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return HTMLResponse('0')
    result = await db.execute(select(Notification).where(Notification.user_id == user_id, Notification.read_at.is_(None)))
    count = len(result.scalars().all())
    return HTMLResponse(str(count))


@router.get('/notifications/peek', response_class=HTMLResponse)
async def web_notifications_peek(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return HTMLResponse('')
    # Show nothing while OTP is disabled (simplify)
    return HTMLResponse('')


@router.get('/notifications', response_class=HTMLResponse)
async def web_notifications(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get all notifications for the user, ordered by newest first
    notifications = (await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(50)
    )).scalars().all()
    
    return templates.TemplateResponse('notifications/list.html', {
        'request': request,
        'user': user,
        'notifications': notifications
    })


@router.post('/notifications/{notification_id}/read')
async def web_notification_mark_read(
    request: Request,
    notification_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    notification = (await db.execute(
        select(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user_id)
    )).scalar_one_or_none()
    
    if notification:
        from datetime import datetime
        notification.read_at = datetime.utcnow()
        await db.commit()
        
        # Smart navigation based on notification type
        if notification.url:
            return RedirectResponse(notification.url, status_code=303)
        elif notification.type == 'meeting' and notification.related_id:
            return RedirectResponse(f'/web/meetings?highlight={notification.related_id}', status_code=303)
        elif notification.type in ['task', 'assignment'] and notification.related_id:
            return RedirectResponse(f'/web/tasks/my?highlight={notification.related_id}', status_code=303)
        elif notification.type == 'message':
            # For messages, navigate to the chat
            return RedirectResponse(notification.url or '/web/chats', status_code=303)
    
    return RedirectResponse('/web/notifications', status_code=303)


@router.post('/notifications/{notification_id}/delete')
async def web_notification_delete(
    request: Request,
    notification_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    notification = (await db.execute(
        select(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user_id)
    )).scalar_one_or_none()
    
    if notification:
        await db.delete(notification)
        await db.commit()
    
    return RedirectResponse('/web/notifications', status_code=303)


@router.post('/notifications/{notification_id}/dismiss')
async def web_notification_dismiss(
    request: Request,
    notification_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Mark notification popup as dismissed (auto-dismiss after 1 minute)"""
    user_id = request.session.get('user_id')
    if not user_id:
        return HTMLResponse('', status_code=401)
    
    notification = (await db.execute(
        select(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user_id)
    )).scalar_one_or_none()
    
    if notification:
        from datetime import datetime
        notification.dismissed_at = datetime.utcnow()
        await db.commit()
    
    return HTMLResponse('OK')


@router.get('/notifications/unread', response_class=HTMLResponse)
async def web_notifications_unread(request: Request, db: AsyncSession = Depends(get_session)):
    """Get unread and undismissed notifications for popup display"""
    user_id = request.session.get('user_id')
    if not user_id:
        return HTMLResponse('[]')
    
    notifications = (await db.execute(
        select(Notification)
        .where(
            Notification.user_id == user_id,
            Notification.read_at.is_(None),
            Notification.dismissed_at.is_(None)
        )
        .order_by(Notification.created_at.desc())
        .limit(5)
    )).scalars().all()
    
    import json
    notification_data = [{
        'id': n.id,
        'type': n.type,
        'message': n.message,
        'url': n.url,
        'related_id': n.related_id,
        'created_at': n.created_at.isoformat() if n.created_at else None
    } for n in notifications]
    
    return HTMLResponse(json.dumps(notification_data), media_type='application/json')


@router.post('/notifications/mark-all-read')
async def web_notifications_mark_all_read(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    from datetime import datetime
    await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id, Notification.read_at.is_(None))
    )
    
    # Update all unread notifications
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id, Notification.read_at.is_(None))
    )
    notifications = result.scalars().all()
    
    for notification in notifications:
        notification.read_at = datetime.utcnow()
    
    await db.commit()
    return RedirectResponse('/web/notifications', status_code=303)


# --------------------------
# User Management (all users can view, only admins can create)
# --------------------------
@router.get('/admin/users', response_class=HTMLResponse)
async def web_admin_users_list(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # All users can view the user list (not just admins)
    # Get all users in the workspace
    users = (
        await db.execute(
            select(User)
            .where(User.workspace_id == user.workspace_id)
            .order_by(User.username)
        )
    ).scalars().all()
    
    return templates.TemplateResponse(
        'admin/users_list.html',
        {
            'request': request,
            'user': user,
            'users': users,
        },
    )


@router.get('/admin/users/create', response_class=HTMLResponse)
async def web_admin_create_user(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return templates.TemplateResponse(
        'admin/create_user.html',
        {
            'request': request,
            'user': user,
            'error': None,
            'success': None,
        },
    )


@router.post('/admin/users/create')
async def web_admin_create_user_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    is_admin: bool = Form(False),
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Import validation function
    from app.core.security import validate_password
    
    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return templates.TemplateResponse(
            'admin/create_user.html',
            {
                'request': request,
                'user': user,
                'error': error_msg,
                'success': None,
            },
            status_code=400
        )
    
    # Check if username already exists
    exists = await db.execute(select(User).where(User.username == username))
    if exists.scalar_one_or_none():
        return templates.TemplateResponse(
            'admin/create_user.html',
            {
                'request': request,
                'user': user,
                'error': 'Username already taken',
                'success': None,
            },
            status_code=400
        )
    
    # Check if email is already used
    if email:
        exists = await db.execute(select(User).where(User.email == email))
        if exists.scalar_one_or_none():
            return templates.TemplateResponse(
                'admin/create_user.html',
                {
                    'request': request,
                    'user': user,
                    'error': 'Email already in use',
                    'success': None,
                },
                status_code=400
            )
    
    # Create new user
    new_user = User(
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        email=email,
        workspace_id=user.workspace_id,
        is_admin=is_admin,
        profile_completed=True,  # Admin sets all details
        email_verified=True,
        is_active=True,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return templates.TemplateResponse(
        'admin/create_user.html',
        {
            'request': request,
            'user': user,
            'error': None,
            'success': f'User "{username}" created successfully!',
        },
    )


@router.post('/admin/users/{user_id}/deactivate')
async def web_admin_deactivate_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Can't deactivate yourself
    if user_id == current_user_id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    
    # Get the user to deactivate
    target_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Must be in same workspace
    if target_user.workspace_id != current_user.workspace_id:
        raise HTTPException(status_code=403, detail="User not in your workspace")
    
    # Deactivate the user
    target_user.is_active = False
    await db.commit()
    
    return RedirectResponse('/web/admin/users', status_code=303)


# User Activity Reports
# --------------------------
@router.get('/admin/reports/user-activity', response_class=HTMLResponse)
async def web_admin_user_activity_report(
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    """Admin page to generate user activity reports"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get all users in workspace
    users = (
        await db.execute(
            select(User)
            .where(User.workspace_id == user.workspace_id)
            .order_by(User.full_name, User.username)
        )
    ).scalars().all()
    
    return templates.TemplateResponse(
        'admin/user_activity_report.html',
        {
            'request': request,
            'user': user,
            'users': users,
        },
    )


@router.get('/admin/reports/user-activity/{target_user_id}/pdf')
async def web_admin_generate_user_activity_pdf(
    request: Request,
    target_user_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    """Generate PDF report of user activity"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get target user
    target_user = (await db.execute(select(User).where(User.id == target_user_id))).scalar_one_or_none()
    if not target_user or target_user.workspace_id != user.workspace_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Parse date range
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_dt = datetime.now() - timedelta(days=30)
    
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    else:
        end_dt = datetime.now() + timedelta(days=1)
    
    # Gather activity data
    from sqlalchemy import text
    
    # 1. Tasks created - filter by workspace through project
    tasks_created = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Task.creator_id == target_user_id)
        .where(Task.created_at >= start_dt)
        .where(Task.created_at < end_dt)
        .order_by(Task.created_at.desc())
    )).scalars().all()
    
    # 2. Task assignments - filter by workspace through project
    task_assignments = (await db.execute(
        select(Task, Assignment)
        .join(Assignment, Task.id == Assignment.task_id)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Assignment.assignee_id == target_user_id)
        .where(Task.created_at >= start_dt)
        .where(Task.created_at < end_dt)
        .order_by(Task.created_at.desc())
    )).all()
    
    # 3. Task edits - filter by workspace through task->project
    try:
        task_edits_result = await db.execute(
            text("""
                SELECT th.id, th.task_id, th.editor_id, th.field, th.old_value, th.new_value, th.created_at
                FROM taskhistory th
                JOIN task t ON th.task_id = t.id
                JOIN project p ON t.project_id = p.id
                WHERE th.editor_id = :user_id
                AND p.workspace_id = :workspace_id
                AND th.created_at >= :start_dt
                AND th.created_at < :end_dt
                ORDER BY th.created_at DESC
            """),
            {"user_id": target_user_id, "workspace_id": target_user.workspace_id, "start_dt": start_dt, "end_dt": end_dt}
        )
        task_edits_raw = task_edits_result.fetchall()
        # Convert to objects with attributes for compatibility
        class TaskEditRow:
            def __init__(self, row):
                self.id, self.task_id, self.editor_id, self.field, self.old_value, self.new_value, created_at_val = row
                # Parse created_at if it's a string
                if isinstance(created_at_val, str):
                    try:
                        self.created_at = datetime.fromisoformat(created_at_val.replace('Z', '+00:00'))
                    except Exception:
                        self.created_at = datetime.now()
                else:
                    self.created_at = created_at_val
        task_edits = [TaskEditRow(row) for row in task_edits_raw]
    except Exception as e:
        logger.error(f"Error fetching task edits: {e}")
        task_edits = []
    
    # 4. Comments - filter by workspace through task->project
    try:
        comments_result = await db.execute(
            text("""
                SELECT c.id, c.task_id, c.author_id, c.content, c.created_at 
                FROM comment c
                JOIN task t ON c.task_id = t.id
                JOIN project p ON t.project_id = p.id
                WHERE c.author_id = :user_id 
                AND p.workspace_id = :workspace_id
                AND c.created_at >= :start_dt 
                AND c.created_at < :end_dt 
                ORDER BY c.created_at DESC
            """),
            {"user_id": target_user_id, "workspace_id": target_user.workspace_id, "start_dt": start_dt, "end_dt": end_dt}
        )
        comments = comments_result.fetchall()
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        comments = []
    
    # 5. Projects created - filter by workspace
    projects_created = (await db.execute(
        select(Project)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Project.owner_id == target_user_id)
        .where(Project.created_at >= start_dt)
        .where(Project.created_at < end_dt)
        .order_by(Project.created_at.desc())
    )).scalars().all()
    
    # 6. Activities logged - filter by workspace
    activities = (await db.execute(
        select(Activity)
        .where(Activity.workspace_id == target_user.workspace_id)
        .where(Activity.created_by == target_user_id)
        .where(Activity.created_at >= start_dt)
        .where(Activity.created_at < end_dt)
        .order_by(Activity.created_at.desc())
    )).scalars().all()
    
    tickets_closed = []
    ticket_comments = []
    tickets_assigned = []
    
    # Generate PDF
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    
    # Create PDF in memory
    import io
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=20,
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=8,
    )
    
    # Title
    elements.append(Paragraph(f"User Activity Report", title_style))
    elements.append(Paragraph(f"{target_user.full_name or target_user.username}", heading_style))
    elements.append(Paragraph(
        f"Period: {start_dt.strftime('%B %d, %Y')} - {end_dt.strftime('%B %d, %Y')}",
        subheading_style
    ))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subheading_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary section with enhanced metrics
    elements.append(Paragraph("Activity Summary", heading_style))
    summary_data = [
        ['Activity Type', 'Count'],
        ['Tasks Created', str(len(tasks_created))],
        ['Task Assignments Received', str(len(task_assignments))],
        ['Task Edits Made', str(len(task_edits))],
        ['Task Comments Posted', str(len(comments))],
        ['Projects Created', str(len(projects_created))],
        ['Activities Logged (Calls/Emails/Meetings)', str(len(activities))],
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # OVERDUE TASKS SECTION (Critical!)
    from datetime import date as date_type
    now = datetime.now()
    now_date = now.date()
    
    # Helper function to handle both date and datetime
    def is_overdue(due_date):
        if not due_date:
            return False
        # Convert to date if it's a datetime
        if isinstance(due_date, datetime):
            due_date = due_date.date()
        return due_date < now_date
    
    overdue_tasks = []
    for task in tasks_created:
        if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
            overdue_tasks.append(task)
    for task, assignment in task_assignments:
        if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
            if task not in overdue_tasks:
                overdue_tasks.append(task)
    
    if overdue_tasks:
        elements.append(Paragraph("⚠️ OVERDUE TASKS", heading_style))
        overdue_data = [['Task Title', 'Due Date', 'Days Overdue', 'Priority', 'Status']]
        for task in sorted(overdue_tasks, key=lambda t: t.due_date if isinstance(t.due_date, date_type) else t.due_date.date()):
            task_due_date = task.due_date if isinstance(task.due_date, date_type) else task.due_date.date()
            days_overdue = (now_date - task_due_date).days
            overdue_data.append([
                Paragraph(task.title, styles['Normal']),
                task_due_date.strftime('%Y-%m-%d'),
                str(days_overdue),
                task.priority.value.title(),
                task.status.value.replace('_', ' ').title(),
            ])
        
        overdue_table = Table(overdue_data, colWidths=[2.3*inch, 1*inch, 1.2*inch, 0.9*inch, 1*inch])
        overdue_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightpink, colors.mistyrose]),
        ]))
        elements.append(overdue_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Tasks Created with enhanced details
    elements.append(Paragraph("Tasks Created", heading_style))
    if tasks_created:
        task_data = [['Date Created', 'Title', 'Due Date', 'Priority', 'Status']]
        for task in tasks_created:
            due_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No due date'
            if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
                due_str += ' (OVERDUE)'
            task_data.append([
                task.created_at.strftime('%Y-%m-%d'),
                task.title[:35],
                due_str,
                task.priority.value.title(),
                task.status.value.replace('_', ' ').title(),
            ])
        
        task_table = Table(task_data, colWidths=[1.1*inch, 2*inch, 1.3*inch, 0.9*inch, 1.1*inch])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(task_table)
    else:
        elements.append(Paragraph("No tasks created during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Task Assignments Received
    elements.append(Paragraph("Task Assignments Received", heading_style))
    if task_assignments:
        assignment_data = [['Date', 'Title', 'Assigned By', 'Due Date', 'Status']]
        for task, assignment in task_assignments:
            # Task creator is the one who assigned it
            assigner = (await db.execute(select(User).where(User.id == task.creator_id))).scalar_one_or_none()
            assigner_name = assigner.full_name or assigner.username if assigner else 'Unknown'
            due_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'
            if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
                due_str += ' (LATE)'
            assignment_data.append([
                task.created_at.strftime('%Y-%m-%d'),
                Paragraph(task.title, styles['Normal']),
                Paragraph(assigner_name, styles['Normal']),
                due_str,
                task.status.value.replace('_', ' ').title(),
            ])
        
        assignment_table = Table(assignment_data, colWidths=[1*inch, 1.8*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        assignment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(assignment_table)
    else:
        elements.append(Paragraph("No task assignments received during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Task Edits
    elements.append(Paragraph("Recent Task Edits", heading_style))
    if task_edits:
        edit_data = [['Date', 'Task ID', 'Field Changed', 'Old Value', 'New Value']]
        for edit in task_edits:
            edit_data.append([
                edit.created_at.strftime('%Y-%m-%d %H:%M'),
                str(edit.task_id),
                edit.field.replace('_', ' ').title(),
                Paragraph(edit.old_value or 'None', styles['Normal']),
                Paragraph(edit.new_value or 'None', styles['Normal']),
            ])
        
        edit_table = Table(edit_data, colWidths=[1.3*inch, 0.7*inch, 1.2*inch, 1.5*inch, 1.5*inch])
        edit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(edit_table)
    else:
        elements.append(Paragraph("No task edits made during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Comments
    elements.append(Paragraph("Recent Comments", heading_style))
    if comments:
        comment_data = [['Date', 'Task ID', 'Comment']]
        for comment in comments:
            # comment is a tuple: (id, task_id, author_id, content, created_at)
            comment_id, task_id, author_id, content, created_at = comment
            comment_data.append([
                created_at.strftime('%Y-%m-%d %H:%M') if isinstance(created_at, datetime) else str(created_at)[:16],
                str(task_id),
                Paragraph(content or '', styles['Normal']),
            ])
        
        comment_table = Table(comment_data, colWidths=[1.5*inch, 0.8*inch, 4*inch])
        comment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        elements.append(comment_table)
    else:
        elements.append(Paragraph("No comments posted during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Projects Created
    elements.append(Paragraph("Projects Created", heading_style))
    if projects_created:
        from app.models.project_member import ProjectMember
        project_data = [['Date', 'Project Name', 'Status', 'Members']]
        for project in projects_created:
            member_count = (await db.execute(
                select(ProjectMember).where(ProjectMember.project_id == project.id)
            )).scalars().all()
            project_data.append([
                project.created_at.strftime('%Y-%m-%d'),
                Paragraph(project.name, styles['Normal']),
                project.status.value.title(),
                str(len(member_count)),
            ])
        
        project_table = Table(project_data, colWidths=[1.1*inch, 3*inch, 1.1*inch, 1.1*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lavender]),
        ]))
        elements.append(project_table)
    else:
        elements.append(Paragraph("No projects created during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Activities Logged (Calls, Emails, Meetings, Notes)
    elements.append(Paragraph("Activities Logged (Calls, Emails, Meetings, Notes)", heading_style))
    if activities:
        activity_data = [['Date', 'Type', 'Subject', 'Related To']]
        for activity in activities:
            related = ''
            if activity.project_id:
                proj = (await db.execute(select(Project).where(Project.id == activity.project_id))).scalar_one_or_none()
                related = f"Project: {proj.name[:20]}" if proj else 'Project'
            elif activity.contact_id:
                related = f'Contact ID: {activity.contact_id}'
            
            activity_data.append([
                activity.created_at.strftime('%Y-%m-%d'),
                activity.activity_type.replace('_', ' ').title(),
                Paragraph(activity.subject or '', styles['Normal']),
                Paragraph(related, styles['Normal']),
            ])
        
        activity_table = Table(activity_data, colWidths=[1*inch, 1.1*inch, 2.5*inch, 1.7*inch])
        activity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgoldenrodyellow]),
        ]))
        elements.append(activity_table)
    else:
        elements.append(Paragraph("No activities logged during this period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    # Return Excel file
    from fastapi.responses import StreamingResponse
    filename = f"user_activity_{target_user.username}_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"
    return StreamingResponse(
        buffer,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@router.get('/admin/reports/user-activity/{target_user_id}/view', response_class=HTMLResponse)
async def web_admin_user_activity_view(
    request: Request,
    target_user_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    """View HTML report of user activity with comprehensive metrics"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get target user
    target_user = (await db.execute(select(User).where(User.id == target_user_id))).scalar_one_or_none()
    if not target_user or target_user.workspace_id != user.workspace_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get workspace for timezone
    workspace = (await db.execute(
        select(Workspace).where(Workspace.id == user.workspace_id)
    )).scalar_one_or_none()
    
    # Parse date range
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_dt = datetime.now() - timedelta(days=30)
    
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    else:
        end_dt = datetime.now() + timedelta(days=1)
    
    from sqlalchemy import text
    from datetime import date as date_type
    
    now = datetime.now()
    now_date = now.date()
    
    def is_overdue(due_date):
        if not due_date:
            return False
        if isinstance(due_date, datetime):
            due_date = due_date.date()
        return due_date < now_date
    
    # Gather activity data
    # 1. Tasks created - filter by workspace through project
    tasks_created = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Task.creator_id == target_user_id)
        .where(Task.created_at >= start_dt)
        .where(Task.created_at < end_dt)
        .order_by(Task.created_at.desc())
    )).scalars().all()
    
    # Get project names for tasks
    tasks_with_project = []
    for task in tasks_created:
        project = None
        if task.project_id:
            project = (await db.execute(select(Project).where(Project.id == task.project_id))).scalar_one_or_none()
        tasks_with_project.append({
            'id': task.id,
            'title': task.title,
            'project_name': project.name if project else None,
            'created_at': task.created_at,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'priority': task.priority.value,
            'status': task.status.value,
        })
    
    # 2. Task assignments with details - filter by workspace through project
    task_assignments_raw = (await db.execute(
        select(Task, Assignment)
        .join(Assignment, Task.id == Assignment.task_id)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Assignment.assignee_id == target_user_id)
        .where(Task.created_at >= start_dt)
        .where(Task.created_at < end_dt)
        .order_by(Task.created_at.desc())
    )).all()
    
    task_assignments = []
    for task, assignment in task_assignments_raw:
        assigner = (await db.execute(select(User).where(User.id == task.creator_id))).scalar_one_or_none()
        # Calculate time spent on task (timeentry table may not exist)
        time_spent = 0
        try:
            time_entries_result = await db.execute(
                text("""
                    SELECT SUM(duration_hours) as total FROM timeentry 
                    WHERE task_id = :task_id AND user_id = :user_id
                """),
                {"task_id": task.id, "user_id": target_user_id}
            )
            time_spent = time_entries_result.scalar() or 0
        except Exception:
            pass  # timeentry table doesn't exist
        
        task_assignments.append({
            'id': task.id,
            'title': task.title,
            'assigned_by': assigner.full_name or assigner.username if assigner else 'Unknown',
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'status': task.status.value,
            'time_spent_hours': round(time_spent, 1) if time_spent else None,
        })
    
    # 3. Task edits - filter by workspace through task->project
    try:
        task_edits_result = await db.execute(
            text("""
                SELECT th.id, th.task_id, th.editor_id, th.field, th.old_value, th.new_value, th.created_at
                FROM taskhistory th
                JOIN task t ON th.task_id = t.id
                JOIN project p ON t.project_id = p.id
                WHERE th.editor_id = :user_id
                AND p.workspace_id = :workspace_id
                AND th.created_at >= :start_dt
                AND th.created_at < :end_dt
                ORDER BY th.created_at DESC
            """),
            {"user_id": target_user_id, "workspace_id": target_user.workspace_id, "start_dt": start_dt, "end_dt": end_dt}
        )
        task_edits_raw = task_edits_result.fetchall()
        class TaskEditRow:
            def __init__(self, row):
                self.id, self.task_id, self.editor_id, self.field, self.old_value, self.new_value, created_at_val = row
                # Parse created_at if it's a string
                if isinstance(created_at_val, str):
                    try:
                        self.created_at = datetime.fromisoformat(created_at_val.replace('Z', '+00:00'))
                    except Exception:
                        self.created_at = datetime.now()
                else:
                    self.created_at = created_at_val
        task_edits = [TaskEditRow(row) for row in task_edits_raw]
    except Exception as e:
        logger.error(f"Error fetching task edits: {e}")
        task_edits = []
    
    # 4. Comments - filter by workspace through task->project
    try:
        comments_result = await db.execute(
            text("""
                SELECT c.id, c.task_id, c.author_id, c.content, c.created_at 
                FROM comment c
                JOIN task t ON c.task_id = t.id
                JOIN project p ON t.project_id = p.id
                WHERE c.author_id = :user_id 
                AND p.workspace_id = :workspace_id
                AND c.created_at >= :start_dt 
                AND c.created_at < :end_dt 
                ORDER BY c.created_at DESC
            """),
            {"user_id": target_user_id, "workspace_id": target_user.workspace_id, "start_dt": start_dt, "end_dt": end_dt}
        )
        comments = comments_result.fetchall()
    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        comments = []
    
    # 5. Projects created - filter by workspace
    projects_created = (await db.execute(
        select(Project)
        .where(Project.workspace_id == target_user.workspace_id)
        .where(Project.owner_id == target_user_id)
        .where(Project.created_at >= start_dt)
        .where(Project.created_at < end_dt)
        .order_by(Project.created_at.desc())
    )).scalars().all()
    
    # 6. Activities logged - filter by workspace
    activities = (await db.execute(
        select(Activity)
        .where(Activity.workspace_id == target_user.workspace_id)
        .where(Activity.created_by == target_user_id)
        .where(Activity.created_at >= start_dt)
        .where(Activity.created_at < end_dt)
        .order_by(Activity.created_at.desc())
    )).scalars().all()
    
    tickets_closed = []
    tickets_assigned = []
    ticket_comments = []

        # Calculate overdue tasks
    overdue_tasks = []
    all_assigned_task_ids = set()
    for task, _ in task_assignments_raw:
        all_assigned_task_ids.add(task.id)
        if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
            task_due = task.due_date if isinstance(task.due_date, date_type) else task.due_date.date()
            overdue_tasks.append({
                'id': task.id,
                'title': task.title,
                'due_date': task_due.strftime('%Y-%m-%d'),
                'days_overdue': (now_date - task_due).days,
                'priority': task.priority.value,
                'status': task.status.value,
            })
    
    for task in tasks_created:
        if task.id not in all_assigned_task_ids:
            if task.due_date and is_overdue(task.due_date) and task.status.value not in ['done', 'completed', 'archived']:
                task_due = task.due_date if isinstance(task.due_date, date_type) else task.due_date.date()
                overdue_tasks.append({
                    'id': task.id,
                    'title': task.title,
                    'due_date': task_due.strftime('%Y-%m-%d'),
                    'days_overdue': (now_date - task_due).days,
                    'priority': task.priority.value,
                    'status': task.status.value,
                })
    
    # Calculate total time logged (timeentry table may not exist)
    total_hours = 0
    try:
        total_time_result = await db.execute(
            text("""
                SELECT SUM(duration_hours) as total FROM timeentry 
                WHERE user_id = :user_id 
                AND start_time >= :start_dt 
                AND start_time < :end_dt
            """),
            {"user_id": target_user_id, "start_dt": start_dt, "end_dt": end_dt}
        )
        total_hours = total_time_result.scalar() or 0
    except Exception:
        pass  # timeentry table doesn't exist
    
    # Calculate completed tasks
    completed_count = sum(1 for t, _ in task_assignments_raw if t.status.value in ['done', 'completed'])
    completion_rate = round((completed_count / len(task_assignments_raw) * 100) if task_assignments_raw else 0, 1)
    
    # Calculate average time per task
    tasks_with_time = [t for t in task_assignments if t['time_spent_hours']]
    avg_time_per_task = round(sum(t['time_spent_hours'] for t in tasks_with_time) / len(tasks_with_time), 1) if tasks_with_time else 0
    
    # Count active projects (projectmember table may not exist)
    active_projects = 0
    try:
        active_projects_result = await db.execute(
            text("""
                SELECT COUNT(DISTINCT project_id) FROM projectmember 
                WHERE user_id = :user_id
            """),
            {"user_id": target_user_id}
        )
        active_projects = active_projects_result.scalar() or 0
    except Exception:
        pass  # projectmember table doesn't exist
    
    # Build recent activity timeline
    recent_activity = []
    
    for task in tasks_created[:10]:
        recent_activity.append({
            'type': 'task_created',
            'description': f'Created task: {task.title[:50]}',
            'detail': None,
            'created_at': task.created_at,
        })
    
    for task, _ in task_assignments_raw[:10]:
        if task.status.value in ['done', 'completed']:
            recent_activity.append({
                'type': 'task_completed',
                'description': f'Completed task: {task.title[:50]}',
                'detail': None,
                'created_at': task.updated_at or task.created_at,
            })
    

    
    for comment in comments[:10]:
        # comment[4] may be string or datetime from raw SQL
        comment_date = comment[4]
        if isinstance(comment_date, str):
            try:
                comment_date = datetime.fromisoformat(comment_date.replace('Z', '+00:00'))
            except Exception:
                comment_date = None
        recent_activity.append({
            'type': 'comment',
            'description': f'Commented on task #{comment[1]}',
            'detail': (comment[3] or '')[:60],
            'created_at': comment_date,
        })
    
    # Sort by date - ensure all values are datetime
    def get_sort_date(x):
        dt = x['created_at']
        if dt is None:
            return datetime.min
        if isinstance(dt, str):
            try:
                return datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except Exception:
                return datetime.min
        return dt
    
    recent_activity.sort(key=get_sort_date, reverse=True)
    
    # Prepare summary data
    summary = {
        'tasks_created': len(tasks_created),
        'tasks_assigned': len(task_assignments),
        'task_edits': len(task_edits),
        'comments': len(comments),
        'projects_created': len(projects_created),
        'activities': len(activities),
        'tickets_assigned': len(tickets_assigned),
        'ticket_comments': len(ticket_comments),
        'tickets_closed': len(tickets_closed),
    }
    
    # Prepare metrics
    metrics = {
        'tasks_assigned': len(task_assignments),
        'tasks_completed': completed_count,
        'completion_rate': completion_rate,
        'overdue_tasks': len(overdue_tasks),
        'total_hours': round(total_hours, 1),
        'tickets_closed': len(tickets_closed),
        'avg_time_per_task': avg_time_per_task,
        'on_time_completion': round(100 - (len(overdue_tasks) / max(len(task_assignments), 1) * 100), 1),
        'avg_days_to_complete': 3,  # Would need more complex calculation
        'active_projects': active_projects,
    }
    
    return templates.TemplateResponse(
        'admin/user_activity_view.html',
        {
            'request': request,
            'user': user,
            'target_user': target_user,
            'workspace': workspace,
            'start_date': start_dt.strftime('%Y-%m-%d'),
            'end_date': (end_dt - timedelta(days=1)).strftime('%Y-%m-%d'),
            'now': datetime.now(),
            'summary': summary,
            'metrics': metrics,
            'overdue_tasks': sorted(overdue_tasks, key=lambda x: x['days_overdue'], reverse=True),
            'tasks_created': tasks_with_project,
            'task_assignments': task_assignments,
            'tickets_assigned': tickets_assigned,
            'tickets_closed': tickets_closed,
            'recent_activity': recent_activity[:25],
        },
    )


@router.post('/admin/users/{user_id}/activate')
async def web_admin_activate_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get the user to activate
    target_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Must be in same workspace
    if target_user.workspace_id != current_user.workspace_id:
        raise HTTPException(status_code=403, detail="User not in your workspace")
    
    # Activate the user
    target_user.is_active = True
    await db.commit()
    
    return RedirectResponse('/web/admin/users', status_code=303)


@router.post('/admin/users/{user_id}/toggle-admin')
async def web_admin_toggle_admin(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Can't modify your own admin rights
    if user_id == current_user_id:
        raise HTTPException(status_code=400, detail="Cannot modify your own admin rights")
    
    # Get the target user
    target_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Must be in same workspace
    if target_user.workspace_id != current_user.workspace_id:
        raise HTTPException(status_code=403, detail="User not in your workspace")
    
    # Toggle admin status
    target_user.is_admin = not target_user.is_admin
    await db.commit()
    
    return RedirectResponse('/web/admin/users', status_code=303)






@router.post('/admin/users/{user_id}/delete')
async def web_admin_delete_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Can't delete yourself
    if user_id == current_user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    # Get the user to delete
    target_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Must be in same workspace
    if target_user.workspace_id != current_user.workspace_id:
        raise HTTPException(status_code=403, detail="User not in your workspace")
    
    # Hard delete: Remove user from database
    await db.delete(target_user)
    await db.commit()
    
    return RedirectResponse('/web/admin/users', status_code=303)


@router.post('/admin/users/{user_id}/change-password')
async def web_admin_change_user_password(
    request: Request,
    user_id: int,
    new_password: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get the target user
    target_user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Must be in same workspace
    if target_user.workspace_id != current_user.workspace_id:
        raise HTTPException(status_code=403, detail="User not in your workspace")
    
    # Validate password length
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Hash and update password
    from app.core.security import get_password_hash
    target_user.hashed_password = get_password_hash(new_password)
    
    await db.commit()
    
    return RedirectResponse('/web/admin/users', status_code=303)


# --------------------------
# Admin - Database Backup Management
# --------------------------
@router.get('/admin/backups', response_class=HTMLResponse)
async def web_admin_backups(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.backup import backup_manager
    stats = backup_manager.get_backup_stats()
    
    # Get list of all backups (both .db and .zip)
    backups = []
    for backup_file in sorted(
        [f for f in backup_manager.backup_dir.glob("backup_*.*") 
         if f.suffix in ['.db', '.zip'] and 'latest' not in f.name and 'corrupted' not in f.name],
        key=lambda x: x.stat().st_mtime, 
        reverse=True
    ):
        backup_type = "MANUAL" if "_MANUAL_" in backup_file.name else ("AUTO" if "_AUTO_" in backup_file.name else "UPLOADED")
        includes_attachments = backup_file.suffix == '.zip'
        
        backups.append({
            'filename': backup_file.name,
            'type': backup_type,
            'includes_attachments': includes_attachments,
            'size': backup_file.stat().st_size,
            'size_mb': round(backup_file.stat().st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(backup_file.stat().st_mtime).strftime('%d/%m/%Y %H:%M:%S'),
            'created_timestamp': backup_file.stat().st_mtime
        })
    
    # Get recent system logs for display
    from app.models.system_log import SystemLog
    from sqlalchemy import func as sa_func
    try:
        log_count_result = await db.execute(select(sa_func.count()).select_from(SystemLog))
        log_count = log_count_result.scalar() or 0
        recent_logs_result = await db.execute(
            select(SystemLog).order_by(SystemLog.timestamp.desc()).limit(20)
        )
        recent_logs = recent_logs_result.scalars().all()
    except Exception:
        log_count = 0
        recent_logs = []
    
    return templates.TemplateResponse('admin/backups.html', {
        'request': request,
        'user': user,
        'stats': stats,
        'backups': backups,
        'log_count': log_count,
        'recent_logs': recent_logs
    })


@router.post('/admin/backups/create')
async def web_admin_backup_create(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'success': False, 'error': 'Not authenticated'})
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        return JSONResponse({'success': False, 'error': 'Admin access required'})
    
    from app.core.backup import backup_manager
    import asyncio
    
    if backup_manager.backup_status == 'running':
        return JSONResponse({'success': False, 'error': 'A backup is already in progress'})
    
    # Fire-and-forget: start backup in background thread
    async def _run_backup():
        try:
            backup_manager.backup_status = 'running'
            backup_manager.backup_progress = 'Starting backup...'
            backup_manager.backup_result_file = None
            backup_file = await asyncio.to_thread(
                backup_manager.create_backup, is_manual=True, include_attachments=True
            )
            if backup_file:
                backup_manager.backup_status = 'done'
                backup_manager.backup_progress = 'Backup created successfully'
                backup_manager.backup_result_file = backup_file.name
            else:
                backup_manager.backup_status = 'error'
                backup_manager.backup_progress = 'Backup creation failed'
        except Exception as e:
            backup_manager.backup_status = 'error'
            backup_manager.backup_progress = f'Error: {str(e)[:200]}'
    
    asyncio.create_task(_run_backup())
    return JSONResponse({'success': True, 'message': 'Backup started'})


@router.get('/admin/backups/status')
async def web_admin_backup_status(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Poll endpoint for backup progress"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'success': False, 'error': 'Not authenticated'})
    
    from app.core.backup import backup_manager
    return JSONResponse({
        'status': backup_manager.backup_status,
        'progress': backup_manager.backup_progress,
        'filename': backup_manager.backup_result_file
    })


@router.get('/admin/backups/download/{filename}')
async def web_admin_backup_download(
    request: Request,
    filename: str,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.backup import backup_manager
    from fastapi.responses import FileResponse
    
    # Security: prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    backup_path = (backup_manager.backup_dir / filename).resolve()
    # Ensure the resolved path is still inside the backup directory
    if not str(backup_path).startswith(str(backup_manager.backup_dir.resolve())):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    if not backup_path.exists():
        raise HTTPException(status_code=404, detail="Backup file not found")
    
    return FileResponse(
        path=str(backup_path),
        filename=filename,
        media_type='application/octet-stream'
    )


@router.post('/admin/backups/upload')
async def web_admin_backup_upload(
    request: Request,
    backup_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.backup import backup_manager
    
    # Validate file extension
    if not backup_file.filename.endswith(('.db', '.zip')):
        return RedirectResponse('/web/admin/backups?error=invalid_file', status_code=303)
    
    # Read file content
    content = await backup_file.read()
    
    # Save the uploaded backup
    saved_path = backup_manager.save_uploaded_backup(content, backup_file.filename)
    
    if saved_path:
        return RedirectResponse('/web/admin/backups?success=backup_uploaded', status_code=303)
    else:
        return RedirectResponse('/web/admin/backups?error=upload_failed', status_code=303)


@router.post('/admin/backups/restore')
async def web_admin_backup_restore(
    request: Request,
    backup_file: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.backup import backup_manager
    from pathlib import Path
    
    backup_path = backup_manager.backup_dir / backup_file
    if not backup_path.exists():
        raise HTTPException(status_code=404, detail="Backup file not found")
    
    success = backup_manager.restore_from_backup(backup_path)
    
    if success:
        return RedirectResponse('/web/admin/backups?success=restore_complete', status_code=303)
    else:
        return RedirectResponse('/web/admin/backups?error=restore_failed', status_code=303)


@router.post('/admin/backups/delete')
async def web_admin_backup_delete(
    request: Request,
    backup_file: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.backup import backup_manager
    
    # Security: prevent path traversal
    if '..' in backup_file or '/' in backup_file or '\\' in backup_file:
        return RedirectResponse('/web/admin/backups?error=invalid_filename', status_code=303)
    
    success = backup_manager.delete_backup(backup_file)
    
    if success:
        return RedirectResponse('/web/admin/backups?success=backup_deleted', status_code=303)
    else:
        return RedirectResponse('/web/admin/backups?error=delete_failed', status_code=303)


@router.get('/admin/backups/logs/download')
async def web_admin_logs_download(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Download system diagnostic logs as a text file for a given time range."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.models.system_log import SystemLog
    from fastapi.responses import Response
    
    # Parse date range from query params
    from_str = request.query_params.get('from', '')
    to_str = request.query_params.get('to', '')
    level_filter = request.query_params.get('level', '')
    
    try:
        from_dt = datetime.fromisoformat(from_str) if from_str else datetime.utcnow() - timedelta(days=1)
        to_dt = datetime.fromisoformat(to_str) if to_str else datetime.utcnow()
    except ValueError:
        from_dt = datetime.utcnow() - timedelta(days=1)
        to_dt = datetime.utcnow()
    
    # Build query
    query = select(SystemLog).where(
        SystemLog.timestamp >= from_dt,
        SystemLog.timestamp <= to_dt
    )
    
    if level_filter == 'ERROR':
        query = query.where(SystemLog.level == 'ERROR')
    elif level_filter == 'INFO':
        query = query.where(SystemLog.level.in_(['INFO', 'WARN', 'ERROR']))
    # DEBUG = all levels, empty = all levels
    
    query = query.order_by(SystemLog.timestamp.asc())
    
    result = await db.execute(query)
    logs = result.scalars().all()
    
    if not logs:
        return RedirectResponse('/web/admin/backups?error=no_logs', status_code=303)
    
    # Build compact text report
    lines = [
        f"=== System Diagnostic Report ===",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        f"Range: {from_dt.strftime('%Y-%m-%d %H:%M')} to {to_dt.strftime('%Y-%m-%d %H:%M')}",
        f"Filter: {level_filter or 'ALL'}",
        f"Entries: {len(logs)}",
        f"{'='*60}",
        "",
    ]
    
    for log in logs:
        ts = log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{ts}] [{log.level}] [{log.source}] {log.message}"
        if log.details:
            line += f" | {log.details}"
        lines.append(line)
    
    report_text = "\n".join(lines)
    filename = f"system_log_{from_dt.strftime('%Y%m%d')}_{to_dt.strftime('%Y%m%d')}.txt"
    
    return Response(
        content=report_text,
        media_type="text/plain",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


# --------------------------
# Admin - System Updates
# --------------------------

@router.get('/admin/updates')
async def web_admin_updates(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.update_manager import update_manager
    
    try:
        # Get current version
        current_version = await update_manager.get_current_version()
        
        # Get commit history
        commit_history = await update_manager.get_commit_history(limit=30)
    except Exception as e:
        # If update manager fails, provide defaults
        current_version = {
            'hash': 'unknown',
            'message': 'Unable to determine version',
            'date': 'unknown',
            'branch': 'unknown'
        }
        commit_history = []
    
    # Get SSH public key if it exists
    ssh_public_key = None
    from pathlib import Path
    pub_key_path = Path.home() / ".ssh" / "crm_deploy_key.pub"
    if pub_key_path.exists():
        ssh_public_key = pub_key_path.read_text().strip()
    
    return templates.TemplateResponse('admin/updates.html', {
        'request': request,
        'user': user,
        'current_version': current_version,
        'commit_history': commit_history,
        'ssh_public_key': ssh_public_key,
        'success': request.query_params.get('success'),
        'error': request.query_params.get('error')
    })


@router.get('/admin/setup-ssh')
async def web_admin_setup_ssh(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Generate SSH key and display public key for GitHub"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    import subprocess
    from pathlib import Path
    
    home = Path.home()
    ssh_dir = home / ".ssh"
    key_path = ssh_dir / "crm_deploy_key"
    pub_key_path = ssh_dir / "crm_deploy_key.pub"
    
    message = ""
    
    # Create .ssh directory
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    
    # Generate key if it doesn't exist
    if not key_path.exists():
        try:
            subprocess.run([
                "ssh-keygen", "-t", "ed25519",
                "-C", "crm-server-deploy-key",
                "-f", str(key_path),
                "-N", ""
            ], check=True, capture_output=True)
            message = "SSH key generated successfully!"
        except Exception as e:
            message = f"Failed to generate key: {e}"
    else:
        message = "SSH key already exists"
    
    # Add GitHub to known hosts
    try:
        known_hosts = ssh_dir / "known_hosts"
        result = subprocess.run(["ssh-keyscan", "github.com"], capture_output=True, text=True)
        if result.stdout:
            with open(known_hosts, "a") as f:
                f.write(result.stdout)
    except Exception:
        pass
    
    # Update git remote to SSH
    try:
        subprocess.run([
            "git", "remote", "set-url", "origin",
            "git@github.com:dadad132/CRM-Honey.git"
        ], capture_output=True)
    except Exception:
        pass
    
    # Read public key
    ssh_public_key = None
    if pub_key_path.exists():
        ssh_public_key = pub_key_path.read_text().strip()
    
    return templates.TemplateResponse('admin/ssh_setup.html', {
        'request': request,
        'user': user,
        'ssh_public_key': ssh_public_key,
        'message': message
    })


@router.post('/admin/updates/latest')
async def web_admin_update_latest(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.update_manager import update_manager
    
    result = await update_manager.update_to_latest()
    
    if result["success"]:
        # Restart service after update
        await update_manager.restart_service()
        return RedirectResponse('/web/admin/updates?success=update_complete', status_code=303)
    else:
        error_msg = result.get("error", "Unknown error")
        return RedirectResponse(f'/web/admin/updates?error={error_msg}', status_code=303)


@router.post('/admin/updates/rollback')
async def web_admin_update_rollback(
    request: Request,
    commit_hash: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from app.core.update_manager import update_manager
    
    result = await update_manager.rollback_to_commit(commit_hash)
    
    if result["success"]:
        # Restart service after rollback
        await update_manager.restart_service()
        return RedirectResponse('/web/admin/updates?success=rollback_complete', status_code=303)
    else:
        error_msg = result.get("error", "Unknown error")
        return RedirectResponse(f'/web/admin/updates?error={error_msg}', status_code=303)


# Site Settings (Admin Only)
# --------------------------
@router.get('/admin/site-settings', response_class=HTMLResponse)
async def web_admin_site_settings(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Site branding and customization settings"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        return RedirectResponse('/web/dashboard', status_code=303)
    
    # Get workspace settings
    error_message = None
    workspace = None
    try:
        workspace = (await db.execute(
            select(Workspace).where(Workspace.id == user.workspace_id)
        )).scalar_one_or_none()
    except Exception as e:
        # If columns don't exist yet, show migration required message
        if "no such column" in str(e):
            error_message = "Database migration required. Please run: python add_site_settings_columns.py"
        else:
            raise
    
    success_message = request.session.pop('success_message', None)
    if not error_message:
        error_message = request.session.pop('error_message', None)
    
    return templates.TemplateResponse('admin/site_settings.html', {
        'request': request,
        'user': user,
        'workspace': workspace,
        'success_message': success_message,
        'error_message': error_message
    })


@router.post('/admin/site-settings/save')
async def web_admin_site_settings_save(
    request: Request,
    site_title: str = Form(None),
    primary_color: str = Form("#2563eb"),
    timezone: str = Form("UTC"),
    business_hours_start: str = Form("07:30"),
    business_hours_end: str = Form("16:00"),
    business_hours_exclude_weekends: str = Form(None),
    db: AsyncSession = Depends(get_session)
):
    """Save site branding settings"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        return RedirectResponse('/web/dashboard', status_code=303)
    
    try:
        # Update workspace settings
        workspace = (await db.execute(
            select(Workspace).where(Workspace.id == user.workspace_id)
        )).scalar_one_or_none()
        
        if workspace:
            workspace.site_title = site_title if site_title else None
            workspace.primary_color = primary_color
            workspace.timezone = timezone
            
            # Business hours settings
            workspace.business_hours_start = business_hours_start or "07:30"
            workspace.business_hours_end = business_hours_end or "16:00"
            workspace.business_hours_exclude_weekends = business_hours_exclude_weekends == "1"
            
            await db.commit()
            request.session['success_message'] = 'Site settings saved successfully!'
        else:
            request.session['error_message'] = 'Workspace not found'
            
    except Exception as e:
        if "no such column" in str(e):
            request.session['error_message'] = 'Database migration required. Run: python migrations/add_workspace_timezone.py'
        else:
            request.session['error_message'] = f'Failed to save settings: {str(e)}'
    
    return RedirectResponse('/web/admin/site-settings', status_code=303)


@router.post('/admin/site-settings/upload-logo')
async def web_admin_site_settings_upload_logo(
    request: Request,
    logo: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    """Upload site logo"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        return RedirectResponse('/web/dashboard', status_code=303)
    
    try:
        # Validate file type (SVG excluded - can contain XSS scripts)
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']
        if logo.content_type not in allowed_types:
            request.session['error_message'] = 'Invalid file type. Please upload PNG, JPG, or GIF.'
            return RedirectResponse('/web/admin/site-settings', status_code=303)
        
        # Validate file size (max 5MB)
        logo_content = await logo.read()
        if len(logo_content) > 5 * 1024 * 1024:
            request.session['error_message'] = 'Logo file is too large. Maximum size is 5MB.'
            return RedirectResponse('/web/admin/site-settings', status_code=303)
        
        # Create uploads directory if it doesn't exist
        import os
        uploads_dir = os.path.join(os.getcwd(), 'app', 'uploads', 'branding')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Generate unique filename
        import uuid
        from pathlib import Path
        file_extension = Path(logo.filename).suffix
        filename = f"logo_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(uploads_dir, filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(logo_content)
        
        # Update workspace
        workspace = (await db.execute(
            select(Workspace).where(Workspace.id == user.workspace_id)
        )).scalar_one_or_none()
        
        if workspace:
            # Delete old logo if exists
            if hasattr(workspace, 'logo_url') and workspace.logo_url:
                old_path = os.path.join(os.getcwd(), 'app', workspace.logo_url.lstrip('/'))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            workspace.logo_url = f"/uploads/branding/{filename}"
            await db.commit()
            request.session['success_message'] = 'Logo uploaded successfully!'
        
    except Exception as e:
        if "no such column" in str(e):
            request.session['error_message'] = 'Database migration required. Run: python add_site_settings_columns.py'
        else:
            request.session['error_message'] = f'Failed to upload logo: {str(e)}'
    
    return RedirectResponse('/web/admin/site-settings', status_code=303)


# --------------------------
# My tasks view
# --------------------------
@router.get('/my-tasks', response_class=HTMLResponse)
async def web_my_tasks(
    request: Request,
    assignee_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)

    # Convert empty strings to None for integer filters
    assignee_id_int = int(assignee_id) if assignee_id and assignee_id.strip() else None
    project_id_int = int(project_id) if project_id and project_id.strip() else None

    # Non-admin: only tasks assigned to me with optional filters
    if not user.is_admin:
        stmt = (
            select(Task)
            .join(Project, Task.project_id == Project.id)
            .join(Assignment, Assignment.task_id == Task.id)
            .where(Assignment.assignee_id == user_id, Project.workspace_id == user.workspace_id)
        )
        if status and status.strip():
            try:
                st = TaskStatus(status)
                stmt = stmt.where(Task.status == st)
            except Exception:
                pass
        if project_id_int:
            stmt = stmt.where(Task.project_id == project_id_int)
        stmt = stmt.order_by(Task.created_at.desc())
        tasks = (await db.execute(stmt)).scalars().all()
        # Non-admin users only see projects they're assigned to
        from app.models.project_member import ProjectMember
        projects = (
            await db.execute(
                select(Project)
                .join(ProjectMember, Project.id == ProjectMember.project_id)
                .where(
                    ProjectMember.user_id == user_id,
                    Project.workspace_id == user.workspace_id
                )
                .order_by(Project.name)
            )
        ).scalars().all()
        return templates.TemplateResponse(
            'tasks/my.html',
            {
                'request': request,
                'tasks': tasks,
                'is_admin': False,
                'projects': projects,
                'selected': {'status': status, 'project_id': project_id},
            },
        )

    # Admin: show all assigned tasks in the workspace, with assignees listed
    tasks_stmt = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .join(Assignment, Assignment.task_id == Task.id)
        .where(Project.workspace_id == user.workspace_id)
    )
    if assignee_id_int:
        tasks_stmt = tasks_stmt.where(Assignment.assignee_id == assignee_id_int)
    if status and status.strip():
        try:
            st = TaskStatus(status)
            tasks_stmt = tasks_stmt.where(Task.status == st)
        except Exception:
            pass
    if project_id_int:
        tasks_stmt = tasks_stmt.where(Task.project_id == project_id_int)
    tasks_stmt = tasks_stmt.order_by(Task.created_at.desc())
    tasks = (await db.execute(tasks_stmt)).scalars().all()

    # Build assignees map {task_id: ["Name or Email", ...]}
    assocs = (
        await db.execute(
            select(Assignment.task_id, User.full_name, User.email)
            .join(User, Assignment.assignee_id == User.id)
            .join(Task, Assignment.task_id == Task.id)
            .join(Project, Task.project_id == Project.id)
            .where(Project.workspace_id == user.workspace_id)
        )
    ).all()
    assignees_map: dict[int, list[str]] = {}
    for task_id_val, full_name, email in assocs:
        label = (full_name or '').strip() or email
        assignees_map.setdefault(task_id_val, []).append(label)

    users = (
        await db.execute(select(User).where(User.workspace_id == user.workspace_id, User.is_active == True).order_by(User.full_name, User.email))
    ).scalars().all()
    projects = (
        await db.execute(select(Project).where(Project.workspace_id == user.workspace_id).order_by(Project.name))
    ).scalars().all()
    return templates.TemplateResponse(
        'tasks/my.html',
        {
            'request': request,
            'tasks': tasks,
            'is_admin': True,
            'assignees_map': assignees_map,
            'users': users,
            'projects': projects,
            'selected': {'assignee_id': assignee_id, 'status': status, 'project_id': project_id},
        },
    )

# --------------------------
# Projects (minimal to enable navigation)
# --------------------------
@router.get('/projects', response_class=HTMLResponse)
async def web_projects(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Admin: see all projects in workspace (excluding archived)
    # Regular user: only see projects they're assigned to (excluding archived)
    if user.is_admin:
        result = await db.execute(
            select(Project)
            .where(Project.workspace_id == user.workspace_id, Project.is_archived == False)
            .order_by(Project.created_at.desc())
        )
        projects = result.scalars().all()
    else:
        from app.models.project_member import ProjectMember
        result = await db.execute(
            select(Project)
            .join(ProjectMember, Project.id == ProjectMember.project_id)
            .where(
                ProjectMember.user_id == user_id,
                Project.workspace_id == user.workspace_id,
                Project.is_archived == False
            )
            .order_by(Project.created_at.desc())
        )
        projects = result.scalars().all()
    
    # Get workspace for branding
    workspace = await get_workspace_for_user(user_id, db)
    
    return templates.TemplateResponse('projects/index.html', {
        'request': request, 
        'user': user,
        'projects': projects,
        'workspace': workspace
    })


@router.post('/projects/create')
async def web_projects_create(request: Request, name: str = Form(...), description: Optional[str] = Form(None), db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    project = Project(name=name, description=description, owner_id=user_id, workspace_id=user.workspace_id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    # Auto-assign the creator to the project
    from app.models.project_member import ProjectMember
    member = ProjectMember(project_id=project.id, user_id=user_id, assigned_by=user_id)
    db.add(member)
    await db.commit()
    
    return RedirectResponse('/web/projects', status_code=303)


@router.post('/projects/{project_id}/edit')
async def web_projects_edit(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can edit projects
    if not user.is_admin:
        return RedirectResponse('/web/projects', status_code=303)
    
    # Get the project
    result = await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))
    project = result.scalar_one_or_none()
    
    if project:
        form = await request.form()
        project.name = form.get('name', project.name)
        project.description = form.get('description') or None
        project.support_email = form.get('support_email') or None
        # IMAP settings for board email integration
        project.imap_host = form.get('imap_host') or None
        imap_port = form.get('imap_port')
        project.imap_port = int(imap_port) if imap_port else None
        project.imap_username = form.get('imap_username') or None
        # Only update password if provided (don't clear existing)
        imap_password = form.get('imap_password')
        if imap_password:
            project.imap_password = imap_password
        project.imap_use_ssl = form.get('imap_use_ssl') == 'on'
        await db.commit()
    
    return RedirectResponse('/web/projects', status_code=303)


@router.post('/projects/{project_id}/delete')
async def web_projects_delete(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can delete projects
    if not user.is_admin:
        return RedirectResponse('/web/projects', status_code=303)
    
    # Get the project
    result = await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))
    project = result.scalar_one_or_none()
    
    if project:
        await db.delete(project)
        await db.commit()
    
    return RedirectResponse('/web/projects', status_code=303)


@router.post('/projects/{project_id}/archive')
async def web_projects_archive(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    """Archive a project - preserves all data, comments, and attachments"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can archive projects
    if not user.is_admin:
        return RedirectResponse('/web/projects', status_code=303)
    
    # Get the project
    result = await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))
    project = result.scalar_one_or_none()
    
    if project:
        from datetime import datetime
        project.is_archived = True
        project.archived_at = datetime.utcnow()
        await db.commit()
    
    return RedirectResponse('/web/projects', status_code=303)


@router.post('/projects/{project_id}/restore')
async def web_projects_restore(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    """Restore an archived project"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can restore projects
    if not user.is_admin:
        return RedirectResponse('/web/projects/archived', status_code=303)
    
    # Get the project
    result = await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))
    project = result.scalar_one_or_none()
    
    if project:
        project.is_archived = False
        project.archived_at = None
        await db.commit()
    
    return RedirectResponse('/web/projects/archived', status_code=303)


@router.get('/projects/archived', response_class=HTMLResponse)
async def web_projects_archived(request: Request, db: AsyncSession = Depends(get_session)):
    """View archived projects"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get archived projects
    if user.is_admin:
        result = await db.execute(
            select(Project)
            .where(Project.workspace_id == user.workspace_id, Project.is_archived == True)
            .order_by(Project.archived_at.desc())
        )
        projects = result.scalars().all()
    else:
        from app.models.project_member import ProjectMember
        result = await db.execute(
            select(Project)
            .join(ProjectMember, Project.id == ProjectMember.project_id)
            .where(
                ProjectMember.user_id == user_id,
                Project.workspace_id == user.workspace_id,
                Project.is_archived == True
            )
            .order_by(Project.archived_at.desc())
        )
        projects = result.scalars().all()
    
    return templates.TemplateResponse('projects/archived.html', {
        'request': request, 
        'user': user,
        'projects': projects
    })


# --------------------------
# Project Members (Admin only)
# --------------------------
@router.get('/projects/{project_id}/members', response_class=HTMLResponse)
async def web_project_members(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin access required')
    
    # Get project
    project = (await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Get assigned members (exclude deleted users)
    from app.models.project_member import ProjectMember
    assigned_members = (await db.execute(
        select(User, ProjectMember.assigned_at)
        .join(ProjectMember, User.id == ProjectMember.user_id)
        .where(ProjectMember.project_id == project_id)
        .order_by(User.full_name, User.email)
    )).all()
    
    # Get all active workspace users for assignment dropdown
    all_users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id)
        .where(User.is_active == True)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    # Filter out already assigned users
    assigned_user_ids = {m[0].id for m in assigned_members}
    available_users = [u for u in all_users if u.id not in assigned_user_ids]
    
    return templates.TemplateResponse('projects/members.html', {
        'request': request,
        'user': user,
        'project': project,
        'assigned_members': assigned_members,
        'available_users': available_users
    })


@router.post('/projects/{project_id}/members/add')
async def web_project_members_add(
    request: Request, 
    project_id: int, 
    user_identifier: str = Form(...),  # Changed from user_id_to_add to user_identifier 
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin access required')
    
    # Verify project exists in workspace
    project = (await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Find user by username or email in the same workspace
    user_identifier = user_identifier.strip()
    target_user = (await db.execute(
        select(User).where(
            User.workspace_id == user.workspace_id,
            (User.username == user_identifier) | (User.email == user_identifier)
        )
    )).scalar_one_or_none()
    
    if not target_user:
        # User not found - return with error message
        request.session['error_message'] = f'User with username or email "{user_identifier}" not found in your workspace'
        return RedirectResponse(f'/web/projects/{project_id}/members', status_code=303)
    
    # Check if already assigned
    from app.models.project_member import ProjectMember
    existing = (await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == target_user.id
        )
    )).scalar_one_or_none()
    
    if existing:
        request.session['info_message'] = f'User {target_user.full_name or target_user.email} is already assigned to this project'
    else:
        member = ProjectMember(project_id=project_id, user_id=target_user.id, assigned_by=user_id)
        db.add(member)
        await db.commit()
        request.session['success_message'] = f'Successfully added {target_user.full_name or target_user.email} to the project'
    
    return RedirectResponse(f'/web/projects/{project_id}/members', status_code=303)


@router.post('/projects/{project_id}/members/{member_user_id}/remove')
async def web_project_members_remove(
    request: Request, 
    project_id: int, 
    member_user_id: int, 
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin access required')
    
    # Remove the assignment
    from app.models.project_member import ProjectMember
    member = (await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == member_user_id
        )
    )).scalar_one_or_none()
    
    if member:
        await db.delete(member)
        await db.commit()
    
    return RedirectResponse(f'/web/projects/{project_id}/members', status_code=303)


# Project Report
@router.get('/projects/{project_id}/report', response_class=HTMLResponse)
async def web_project_report(
    request: Request, 
    project_id: int, 
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session)
):
    """Project report showing who did what tasks and time spent"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get project
    project = (await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Only admins can access reports
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin access required')
    
    # Parse date range (default to last 30 days)
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_dt = datetime.now() - timedelta(days=30)
        start_date = start_dt.strftime('%Y-%m-%d')
    
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    else:
        end_dt = datetime.now() + timedelta(days=1)
        end_date = (end_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get all tasks for the project
    all_tasks = (await db.execute(
        select(Task).where(Task.project_id == project_id)
    )).scalars().all()
    
    # Get tasks in date range
    tasks_in_range = (await db.execute(
        select(Task).where(
            Task.project_id == project_id,
            Task.created_at >= start_dt,
            Task.created_at < end_dt
        ).order_by(Task.created_at.desc())
    )).scalars().all()
    
    # Get all assignments
    task_ids = [t.id for t in all_tasks]
    assignments = []
    if task_ids:
        assignments = (await db.execute(
            select(Assignment, User)
            .join(User, User.id == Assignment.assignee_id)
            .where(Assignment.task_id.in_(task_ids))
        )).all()
    
    # Build assignees map
    assignees_map = {}  # task_id -> [(name, email), ...]
    for assignment, assignee_user in assignments:
        if assignment.task_id not in assignees_map:
            assignees_map[assignment.task_id] = []
        assignees_map[assignment.task_id].append((
            assignee_user.full_name or assignee_user.username,
            assignee_user.email
        ))
    
    # Get task history for completion dates
    task_completions = {}  # task_id -> completion datetime
    if task_ids:
        completions = (await db.execute(
            select(TaskHistory)
            .where(
                TaskHistory.task_id.in_(task_ids),
                TaskHistory.field == 'status',
                TaskHistory.new_value == 'done'
            )
            .order_by(TaskHistory.created_at.desc())
        )).scalars().all()
        
        for completion in completions:
            if completion.task_id not in task_completions:
                task_completions[completion.task_id] = completion.created_at
    
    # Calculate contributor stats
    contributor_stats = {}  # user_id -> stats
    
    for assignment, assignee_user in assignments:
        uid = assignee_user.id
        if uid not in contributor_stats:
            contributor_stats[uid] = {
                'user': assignee_user,
                'name': assignee_user.full_name or assignee_user.username,
                'email': assignee_user.email,
                'initials': ''.join([n[0].upper() for n in (assignee_user.full_name or assignee_user.email).split()[:2]]),
                'tasks_assigned': 0,
                'tasks_completed': 0,
                'hours_logged': 0.0
            }
        
        # Find the task
        task = next((t for t in all_tasks if t.id == assignment.task_id), None)
        if task:
            contributor_stats[uid]['tasks_assigned'] += 1
            if task.status == TaskStatus.done:
                contributor_stats[uid]['tasks_completed'] += 1
            if task.time_spent_hours:
                contributor_stats[uid]['hours_logged'] += task.time_spent_hours
    
    # Format contributor data
    contributors = []
    for uid, stats in contributor_stats.items():
        completion_rate = round((stats['tasks_completed'] / stats['tasks_assigned'] * 100) if stats['tasks_assigned'] > 0 else 0)
        avg_hours = round(stats['hours_logged'] / stats['tasks_completed'], 1) if stats['tasks_completed'] > 0 else 0
        contributors.append({
            'name': stats['name'],
            'email': stats['email'],
            'initials': stats['initials'],
            'tasks_assigned': stats['tasks_assigned'],
            'tasks_completed': stats['tasks_completed'],
            'completion_rate': completion_rate,
            'hours_logged': round(stats['hours_logged'], 1),
            'avg_hours_per_task': avg_hours
        })
    
    # Sort by tasks completed (descending)
    contributors.sort(key=lambda x: x['tasks_completed'], reverse=True)
    
    # Build task details
    tasks_detail = []
    for task in all_tasks:
        completed_at = task_completions.get(task.id)
        duration_days = None
        if completed_at:
            duration_days = (completed_at - task.created_at).days
        
        tasks_detail.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status.value if hasattr(task.status, 'value') else task.status,
            'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
            'assignees': [a[0] for a in assignees_map.get(task.id, [])],
            'created_at': task.created_at,
            'completed_at': completed_at,
            'time_spent_hours': task.time_spent_hours,
            'duration_days': duration_days
        })
    
    # Sort by created_at descending
    tasks_detail.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Get activity timeline from TaskHistory
    activities = []
    if task_ids:
        history_entries = (await db.execute(
            select(TaskHistory, User, Task)
            .join(User, User.id == TaskHistory.editor_id)
            .join(Task, Task.id == TaskHistory.task_id)
            .where(
                TaskHistory.task_id.in_(task_ids),
                TaskHistory.created_at >= start_dt,
                TaskHistory.created_at < end_dt
            )
            .order_by(TaskHistory.created_at.desc())
            .limit(50)
        )).all()
        
        for history, editor, task in history_entries:
            action = 'updated'
            description = f'updated {history.field}'
            
            if history.field == 'created':
                action = 'created'
                description = 'created the task'
            elif history.field == 'status':
                action = 'status_changed'
                if history.new_value == 'done':
                    action = 'completed'
                    description = 'completed the task'
                else:
                    description = f'changed status from {history.old_value or "none"} to {history.new_value}'
            elif history.field == 'priority':
                description = f'changed priority from {history.old_value or "none"} to {history.new_value}'
            elif history.field == 'assignee':
                description = f'changed assignee'
            
            activities.append({
                'action': action,
                'description': description,
                'user_name': editor.full_name or editor.username,
                'task_title': task.title,
                'created_at': history.created_at
            })
    
    # Calculate summary
    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for t in all_tasks if t.status == TaskStatus.done)
    completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)
    total_hours = round(sum(t.time_spent_hours or 0 for t in all_tasks), 1)
    active_contributors = len(contributor_stats)
    
    summary = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        'total_hours': total_hours,
        'active_contributors': active_contributors
    }
    
    # Get workspace for timezone
    workspace = (await db.execute(
        select(Workspace).where(Workspace.id == user.workspace_id)
    )).scalar_one_or_none()
    
    return templates.TemplateResponse('projects/report.html', {
        'request': request,
        'user': user,
        'project': project,
        'workspace': workspace,
        'start_date': start_date,
        'end_date': end_date,
        'summary': summary,
        'contributors': contributors,
        'tasks_detail': tasks_detail,
        'activities': activities
    })


@router.get('/projects/{project_id}/report/pdf')
async def web_project_report_pdf(
    request: Request, 
    project_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session)
):
    """Generate PDF report for project"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can access reports
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin access required')
    
    # Get project
    project = (await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id)
    )).scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Parse date range
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_dt = datetime.now() - timedelta(days=30)
    
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    else:
        end_dt = datetime.now() + timedelta(days=1)
    
    # Get all tasks for the project
    all_tasks = (await db.execute(
        select(Task).where(Task.project_id == project_id)
    )).scalars().all()
    
    # Get assignments
    task_ids = [t.id for t in all_tasks]
    assignments = []
    if task_ids:
        assignments = (await db.execute(
            select(Assignment, User)
            .join(User, User.id == Assignment.assignee_id)
            .where(Assignment.task_id.in_(task_ids))
        )).all()
    
    # Build assignees map
    assignees_map = {}
    for assignment, assignee_user in assignments:
        if assignment.task_id not in assignees_map:
            assignees_map[assignment.task_id] = []
        assignees_map[assignment.task_id].append(assignee_user.full_name or assignee_user.username)
    
    # Get completion dates
    task_completions = {}
    if task_ids:
        completions = (await db.execute(
            select(TaskHistory)
            .where(
                TaskHistory.task_id.in_(task_ids),
                TaskHistory.field == 'status',
                TaskHistory.new_value == 'done'
            )
            .order_by(TaskHistory.created_at.desc())
        )).scalars().all()
        
        for completion in completions:
            if completion.task_id not in task_completions:
                task_completions[completion.task_id] = completion.created_at
    
    # Calculate contributor stats
    contributor_stats = {}
    for assignment, assignee_user in assignments:
        uid = assignee_user.id
        if uid not in contributor_stats:
            contributor_stats[uid] = {
                'name': assignee_user.full_name or assignee_user.username,
                'tasks_assigned': 0,
                'tasks_completed': 0,
                'hours_logged': 0.0
            }
        
        task = next((t for t in all_tasks if t.id == assignment.task_id), None)
        if task:
            contributor_stats[uid]['tasks_assigned'] += 1
            if task.status == TaskStatus.done:
                contributor_stats[uid]['tasks_completed'] += 1
            if task.time_spent_hours:
                contributor_stats[uid]['hours_logged'] += task.time_spent_hours
    
    # Generate PDF
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    import io
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=20,
    )
    
    # Title
    elements.append(Paragraph(f"Project Report: {project.name}", title_style))
    elements.append(Paragraph(
        f"Period: {start_dt.strftime('%B %d, %Y')} - {(end_dt - timedelta(days=1)).strftime('%B %d, %Y')}",
        styles['Normal']
    ))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for t in all_tasks if t.status == TaskStatus.done)
    completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)
    total_hours = round(sum(t.time_spent_hours or 0 for t in all_tasks), 1)
    
    elements.append(Paragraph("Summary", heading_style))
    summary_data = [
        ['Total Tasks', 'Completed', 'Completion Rate', 'Total Hours'],
        [str(total_tasks), str(completed_tasks), f'{completion_rate}%', f'{total_hours}h']
    ]
    summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Contributor Performance
    elements.append(Paragraph("Contributor Performance", heading_style))
    contrib_headers = ['Contributor', 'Assigned', 'Completed', 'Rate', 'Hours']
    contrib_data = [contrib_headers]
    
    for uid, stats in sorted(contributor_stats.items(), key=lambda x: x[1]['tasks_completed'], reverse=True):
        rate = round((stats['tasks_completed'] / stats['tasks_assigned'] * 100) if stats['tasks_assigned'] > 0 else 0)
        contrib_data.append([
            stats['name'],
            str(stats['tasks_assigned']),
            str(stats['tasks_completed']),
            f'{rate}%',
            f"{round(stats['hours_logged'], 1)}h"
        ])
    
    if len(contrib_data) > 1:
        contrib_table = Table(contrib_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        contrib_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        elements.append(contrib_table)
    else:
        elements.append(Paragraph("No contributors found.", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Task Details
    elements.append(Paragraph("Task Details", heading_style))
    task_headers = ['Task', 'Assignees', 'Status', 'Priority', 'Time']
    task_data = [task_headers]
    
    for task in sorted(all_tasks, key=lambda t: t.created_at, reverse=True):
        assignee_names = ', '.join(assignees_map.get(task.id, ['Unassigned']))
        if len(assignee_names) > 25:
            assignee_names = assignee_names[:22] + '...'
        
        title = task.title
        if len(title) > 35:
            title = title[:32] + '...'
        
        status = task.status.value if hasattr(task.status, 'value') else str(task.status)
        priority = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
        time_str = f"{task.time_spent_hours}h" if task.time_spent_hours else '-'
        
        task_data.append([title, assignee_names, status.title(), priority.title(), time_str])
    
    if len(task_data) > 1:
        task_table = Table(task_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch, 0.7*inch])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        elements.append(task_table)
    else:
        elements.append(Paragraph("No tasks found.", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Return PDF
    from fastapi.responses import StreamingResponse
    filename = f"project_report_{project.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return StreamingResponse(
        buffer,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


# Project detail + simple Kanban
@router.get('/projects/{project_id}', response_class=HTMLResponse)
async def web_project_detail(request: Request, project_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    result = await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Check if user has access to this project (admin or assigned member)
    if not user.is_admin:
        from app.models.project_member import ProjectMember
        member = (await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
        )).scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=403, detail='You do not have access to this project')
    
    # Fetch only non-archived tasks for board view (archived tasks go to the Done tab in tasks/list)
    tasks_result = await db.execute(
        select(Task).where(Task.project_id == project_id, Task.is_archived == False)
    )
    tasks = tasks_result.scalars().all()
    
    # Organize tasks by status for kanban columns
    columns = {
        TaskStatus.todo: [],
        TaskStatus.in_progress: [],
        TaskStatus.blocked: [],
        TaskStatus.done: []
    }
    for t in tasks:
        if t.status in columns:
            columns[t.status].append(t)
    
    # Build assignees map: {task_id: [(full_name, email), ...]}
    assignees_map = {}
    if tasks:
        task_ids = [t.id for t in tasks]
        assignments = (await db.execute(
            select(Assignment.task_id, User.full_name, User.email)
            .join(User, User.id == Assignment.assignee_id)
            .where(Assignment.task_id.in_(task_ids))
        )).all()
        for task_id, full_name, email in assignments:
            if task_id not in assignees_map:
                assignees_map[task_id] = []
            assignees_map[task_id].append((full_name or email, email))
    
    # Fetch subtasks for all tasks
    from app.models.subtask import Subtask
    subtasks_map = {}  # {task_id: [subtasks]}
    subtask_stats = {}  # {task_id: {'total': x, 'completed': y}}
    if tasks:
        task_ids = [t.id for t in tasks]
        subtasks = (await db.execute(
            select(Subtask).where(Subtask.task_id.in_(task_ids)).order_by(Subtask.order)
        )).scalars().all()
        
        for subtask in subtasks:
            if subtask.task_id not in subtasks_map:
                subtasks_map[subtask.task_id] = []
                subtask_stats[subtask.task_id] = {'total': 0, 'completed': 0}
            subtasks_map[subtask.task_id].append(subtask)
            subtask_stats[subtask.task_id]['total'] += 1
            if subtask.is_completed:
                subtask_stats[subtask.task_id]['completed'] += 1
    
    # Fetch attachment counts for all tasks
    from app.models.task_extensions import TaskAttachment
    attachment_counts = {}  # {task_id: count}
    if tasks:
        task_ids = [t.id for t in tasks]
        from sqlalchemy import func
        attachment_result = await db.execute(
            select(TaskAttachment.task_id, func.count(TaskAttachment.id).label('count'))
            .where(TaskAttachment.task_id.in_(task_ids))
            .group_by(TaskAttachment.task_id)
        )
        for task_id, count in attachment_result.all():
            attachment_counts[task_id] = count
    
    # Fetch all active users in workspace for assignment dropdown
    users = (await db.execute(select(User).where(User.workspace_id == user.workspace_id, User.is_active == True).order_by(User.full_name, User.email))).scalars().all()
    return templates.TemplateResponse('projects/detail.html', {
        'request': request, 
        'project': project, 
        'tasks': tasks, 
        'TaskStatus': TaskStatus, 
        'columns': columns,
        'assignees_map': assignees_map,
        'subtasks_map': subtasks_map,
        'subtask_stats': subtask_stats,
        'attachment_counts': attachment_counts,
        'users': users,
        'user': user
    })


# Tasks
@router.post('/tasks/create')
async def web_task_create(request: Request, db: AsyncSession = Depends(get_session)):
    # Get all form data
    form_data = await request.form()
    
    # Extract form fields
    project_id = int(form_data.get('project_id'))
    title = form_data.get('title')
    description = form_data.get('description') or None
    subtasks = form_data.get('subtasks') or None
    priority = form_data.get('priority', 'medium')
    start_date_value = form_data.get('start_date_value') or None
    start_time_value = form_data.get('start_time_value') or None
    due_date_value = form_data.get('due_date_value') or None
    due_time_value = form_data.get('due_time_value') or None
    working_days_list = form_data.getlist('working_days')
    # Customer info (optional)
    customer_name = form_data.get('customer_name') or None
    customer_surname = form_data.get('customer_surname') or None
    customer_email = form_data.get('customer_email') or None
    customer_phone = form_data.get('customer_phone') or None
    
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    # Ensure project belongs to user's workspace
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.workspace_id == user.workspace_id))).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    
    # Ensure user has access to this project (admin or assigned member)
    if not user.is_admin:
        from app.models.project_member import ProjectMember
        member = (await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id
            )
        )).scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=403, detail='You do not have access to this project')
    
    # Parse dates and times
    from datetime import date, time
    start_date = date.fromisoformat(start_date_value) if start_date_value else None
    start_time_obj = time.fromisoformat(start_time_value) if start_time_value else None
    due_date = date.fromisoformat(due_date_value) if due_date_value else None
    due_time_obj = time.fromisoformat(due_time_value) if due_time_value else None
    
    # Parse priority
    from app.models.enums import TaskPriority
    try:
        task_priority = TaskPriority(priority)
    except ValueError:
        task_priority = TaskPriority.medium
    
    # Parse working days (default to Mon-Fri if not provided)
    working_days_str = ','.join(working_days_list) if working_days_list else '0,1,2,3,4'
    
    task = Task(
        title=title, 
        description=description, 
        project_id=project_id,
        creator_id=user_id,
        priority=task_priority,
        start_date=start_date,
        start_time=start_time_obj,
        due_date=due_date,
        due_time=due_time_obj,
        working_days=working_days_str,
        customer_name=customer_name,
        customer_surname=customer_surname,
        customer_email=customer_email,
        customer_phone=customer_phone
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    # Create subtasks if provided
    if subtasks:
        from app.models.subtask import Subtask
        subtask_titles = [title.strip() for title in subtasks.split('\n') if title.strip()]
        for index, subtask_title in enumerate(subtask_titles):
            new_subtask = Subtask(
                task_id=task.id,
                title=subtask_title,
                is_completed=False,
                order=index
            )
            db.add(new_subtask)
        await db.commit()
    
    # Auto-assign task to creator if they're not an admin
    if not user.is_admin:
        from app.models.assignment import Assignment
        assignment = Assignment(task_id=task.id, assignee_id=user_id)
        db.add(assignment)
        await db.commit()
    
    return RedirectResponse(f'/web/projects/{project_id}', status_code=303)


@router.get('/tasks/list')
async def web_tasks_list(
    request: Request,
    tab: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assignee_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    from datetime import date
    
    # Convert empty strings to None for integer filters
    assignee_id_int = int(assignee_id) if assignee_id and assignee_id.strip() else None
    project_id_int = int(project_id) if project_id and project_id.strip() else None
    
    # Build query with filters
    # Admin: see all tasks in workspace
    # Regular user: only tasks from projects they're assigned to OR tasks they created
    if user.is_admin:
        query = (
            select(Task, Project.name.label('project_name'))
            .join(Project, Task.project_id == Project.id)
            .where(Project.workspace_id == user.workspace_id)
        )
    else:
        from app.models.project_member import ProjectMember
        # Get tasks where user is either assigned OR is the creator
        query = (
            select(Task, Project.name.label('project_name'))
            .join(Project, Task.project_id == Project.id)
            .join(ProjectMember, Project.id == ProjectMember.project_id)
            .where(
                ProjectMember.user_id == user_id,
                Project.workspace_id == user.workspace_id,
                or_(
                    Task.creator_id == user_id,  # Tasks created by the user
                    Task.id.in_(  # Tasks assigned to the user
                        select(Assignment.task_id)
                        .where(Assignment.assignee_id == user_id)
                    )
                )
            )
        )
    
    # Tab filtering - only apply if no specific status filter is set
    if not status or not status.strip():
        if tab == 'done':
            query = query.where(Task.status == 'done')
        else:  # Active tasks (default when tab is None, empty, or 'active')
            query = query.where(Task.status.in_(['todo', 'in_progress', 'blocked']))
    
    if status and status.strip():
        query = query.where(Task.status == status)
    if priority and priority.strip():
        query = query.where(Task.priority == priority)
    if project_id_int:
        query = query.where(Task.project_id == project_id_int)
    if assignee_id_int:
        query = query.join(Assignment, Task.id == Assignment.task_id).where(Assignment.assignee_id == assignee_id_int)
    
    query = query.order_by(Task.due_date.asc().nullslast(), Task.priority.desc())
    
    results = (await db.execute(query)).all()
    tasks = []
    project_names = {}
    for task, project_name in results:
        tasks.append(task)
        project_names[task.id] = project_name
    
    # Get assignees for all tasks
    task_ids = [t.id for t in tasks]
    assocs = (await db.execute(
        select(Assignment.task_id, User.full_name, User.email)
        .join(User, Assignment.assignee_id == User.id)
        .where(Assignment.task_id.in_(task_ids) if task_ids else False)
    )).all()
    
    assignees_map: dict[int, list[str]] = {}
    for task_id_val, full_name, email in assocs:
        label = (full_name or '').strip() or email
        assignees_map.setdefault(task_id_val, []).append(label)
    
    # Get all users and projects for filters
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id, User.is_active == True)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    # Get projects user has access to
    if user.is_admin:
        projects = (await db.execute(
            select(Project)
            .where(Project.workspace_id == user.workspace_id)
            .order_by(Project.name)
        )).scalars().all()
    else:
        from app.models.project_member import ProjectMember
        projects = (await db.execute(
            select(Project)
            .join(ProjectMember, Project.id == ProjectMember.project_id)
            .where(
                ProjectMember.user_id == user_id,
                Project.workspace_id == user.workspace_id
            )
            .order_by(Project.name)
        )).scalars().all()
    
    return templates.TemplateResponse('tasks/list.html', {
        'request': request,
        'user': user,
        'tasks': tasks,
        'project_names': project_names,
        'assignees_map': assignees_map,
        'users': users,
        'projects': projects,
        'selected': {
            'tab': tab or 'active',
            'status': status,
            'priority': priority,
            'assignee_id': assignee_id,
            'project_id': project_id,
        },
        'today': date.today(),
    })


@router.get('/tasks/{task_id}')
async def web_task_detail(request: Request, task_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get task with project check
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Get project
    project = (await db.execute(select(Project).where(Project.id == task.project_id))).scalar_one_or_none()
    
    # Get assignments
    assignments = (await db.execute(
        select(User)
        .join(Assignment, User.id == Assignment.assignee_id)
        .where(Assignment.task_id == task_id)
    )).scalars().all()
    
    # Get comments with authors
    comments = (await db.execute(
        select(Comment, User)
        .join(User, Comment.author_id == User.id)
        .where(Comment.task_id == task_id)
        .order_by(Comment.created_at.desc())
    )).all()
    
    # Get attachments for all comments
    comment_ids = [c[0].id for c in comments]
    attachments_by_comment = {}
    if comment_ids:
        attachments = (await db.execute(
            select(CommentAttachment).where(CommentAttachment.comment_id.in_(comment_ids))
        )).scalars().all()
        for attachment in attachments:
            if attachment.comment_id not in attachments_by_comment:
                attachments_by_comment[attachment.comment_id] = []
            attachments_by_comment[attachment.comment_id].append(attachment)
    
    # Check if user can comment (admin or assignee)
    is_assignee = any(a.id == user_id for a in assignments)
    can_comment = user.is_admin or is_assignee
    
    # Get edit history
    history = (await db.execute(
        select(TaskHistory, User)
        .join(User, TaskHistory.editor_id == User.id)
        .where(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.created_at.desc())
    )).all()
    
    # Get all active workspace users
    users = (await db.execute(select(User).where(User.workspace_id == user.workspace_id, User.is_active == True).order_by(User.full_name, User.email))).scalars().all()
    
    # Get subtasks ordered by their order field
    from app.models.subtask import Subtask
    subtasks = (await db.execute(
        select(Subtask).where(Subtask.task_id == task_id).order_by(Subtask.order)
    )).scalars().all()
    
    # Calculate subtask completion stats
    total_subtasks = len(subtasks)
    completed_subtasks = sum(1 for st in subtasks if st.is_completed)
    completion_percentage = int((completed_subtasks / total_subtasks) * 100) if total_subtasks > 0 else 0
    
    # Get task dependencies (blocked by)
    from app.models.task_extensions import TaskDependency
    blocked_by_result = await db.execute(
        select(Task)
        .join(TaskDependency, Task.id == TaskDependency.depends_on_task_id)
        .where(TaskDependency.task_id == task_id)
    )
    blocked_by_tasks = blocked_by_result.scalars().all()
    
    # Get tasks that this task blocks
    blocks_result = await db.execute(
        select(Task)
        .join(TaskDependency, Task.id == TaskDependency.task_id)
        .where(TaskDependency.depends_on_task_id == task_id)
    )
    blocks_tasks = blocks_result.scalars().all()
    
    # Get watchers
    from app.models.task_extensions import TaskWatcher
    watchers_result = await db.execute(
        select(User)
        .join(TaskWatcher, User.id == TaskWatcher.user_id)
        .where(TaskWatcher.task_id == task_id)
    )
    watchers = watchers_result.scalars().all()
    
    # Check if current user is watching
    is_watching = any(w.id == user_id for w in watchers)
    
    # Get available tasks for dependency selection (same project, not this task)
    available_tasks = (await db.execute(
        select(Task)
        .where(Task.project_id == task.project_id, Task.id != task_id, Task.is_archived == False)
        .order_by(Task.title)
    )).scalars().all()
    
    # Get task-level attachments (not comment attachments)
    from app.models.task_extensions import TaskAttachment
    task_attachments = (await db.execute(
        select(TaskAttachment).where(TaskAttachment.task_id == task_id).order_by(TaskAttachment.created_at.desc())
    )).scalars().all()
    
    return templates.TemplateResponse('tasks/detail.html', {
        'request': request,
        'task': task,
        'project': project,
        'assignments': assignments,
        'comments': comments,
        'attachments_by_comment': attachments_by_comment,
        'task_attachments': task_attachments,
        'can_comment': can_comment,
        'history': history,
        'users': users,
        'user': user,
        'subtasks': subtasks,
        'total_subtasks': total_subtasks,
        'completed_subtasks': completed_subtasks,
        'completion_percentage': completion_percentage,
        'blocked_by_tasks': blocked_by_tasks,
        'blocks_tasks': blocks_tasks,
        'watchers': watchers,
        'is_watching': is_watching,
        'available_tasks': available_tasks,
        'TaskStatus': TaskStatus,
        'TaskPriority': TaskPriority
    })


@router.post('/tasks/{task_id}/update')
async def web_task_update(
    request: Request,
    task_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    status: str = Form(...),
    priority: str = Form(...),
    start_date_value: Optional[str] = Form(None),
    start_time_value: Optional[str] = Form(None),
    due_date_value: Optional[str] = Form(None),
    due_time_value: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get task
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Check if task is archived - only admins can edit archived tasks
    if task.is_archived and not user.is_admin:
        raise HTTPException(status_code=403, detail='This task is archived. Only admins can modify it.')
    
    # Check permission: Admin OR assigned to this task
    if not user.is_admin:
        from app.models.assignment import Assignment
        assignment = (await db.execute(
            select(Assignment).where(
                Assignment.task_id == task_id,
                Assignment.assignee_id == user_id
            )
        )).scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=403, detail='You can only edit tasks assigned to you')
    
    # Track changes
    from datetime import date, time
    changes = []
    
    if task.title != title:
        changes.append(('title', task.title, title))
        task.title = title
    
    if task.description != description:
        changes.append(('description', task.description or '', description or ''))
        task.description = description
    
    new_status = TaskStatus(status)
    task_just_completed = False
    if task.status != new_status:
        changes.append(('status', task.status.value, new_status.value))
        old_status_value = task.status.value
        task.status = new_status
        
        # Auto-archive when moved to done
        if new_status.value == 'done':
            task.is_archived = True
            task.archived_at = datetime.utcnow()
            task_just_completed = True  # Flag to send completion notification
        elif old_status_value == 'done' and new_status.value != 'done':
            # Unarchive if moved out of done
            task.is_archived = False
            task.archived_at = None
    
    new_priority = TaskPriority(priority)
    if task.priority != new_priority:
        changes.append(('priority', task.priority.value, new_priority.value))
        task.priority = new_priority
    
    new_start_date = date.fromisoformat(start_date_value) if start_date_value else None
    if task.start_date != new_start_date:
        changes.append(('start_date', str(task.start_date) if task.start_date else '', str(new_start_date) if new_start_date else ''))
        task.start_date = new_start_date
    
    new_start_time = time.fromisoformat(start_time_value) if start_time_value else None
    if task.start_time != new_start_time:
        changes.append(('start_time', str(task.start_time) if task.start_time else '', str(new_start_time) if new_start_time else ''))
        task.start_time = new_start_time
    
    new_due_date = date.fromisoformat(due_date_value) if due_date_value else None
    if task.due_date != new_due_date:
        changes.append(('due_date', str(task.due_date) if task.due_date else '', str(new_due_date) if new_due_date else ''))
        task.due_date = new_due_date
    
    new_due_time = time.fromisoformat(due_time_value) if due_time_value else None
    if task.due_time != new_due_time:
        changes.append(('due_time', str(task.due_time) if task.due_time else '', str(new_due_time) if new_due_time else ''))
        task.due_time = new_due_time
    
    # Save history
    for field, old_value, new_value in changes:
        history_entry = TaskHistory(
            task_id=task_id,
            editor_id=user_id,
            field=field,
            old_value=old_value,
            new_value=new_value
        )
        db.add(history_entry)
    
    await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/complete-with-details')
async def web_task_complete_with_details(
    request: Request,
    task_id: int,
    billable_traveling: Optional[str] = Form(None),
    billable_labour_onsite: Optional[str] = Form(None),
    billable_remote_labour: Optional[str] = Form(None),
    billable_equipment_used: Optional[str] = Form(None),
    non_billable_traveling: Optional[str] = Form(None),
    non_billable_labour_onsite: Optional[str] = Form(None),
    non_billable_remote_labour: Optional[str] = Form(None),
    non_billable_equipment_used: Optional[str] = Form(None),
    completion_notes: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    """Complete task with optional billing/work details"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return RedirectResponse('/web/login', status_code=303)
    
    # Get task and verify access
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(
        Task.id == task_id,
        Project.workspace_id == user.workspace_id
    )
    task = (await db.execute(stmt)).scalar_one_or_none()
    
    if not task:
        return RedirectResponse('/web/projects', status_code=303)
    
    # Record old status for history
    old_status = task.status.value
    
    # Update task to done
    task.status = TaskStatus.done
    task.updated_at = datetime.utcnow()
    task.is_archived = True
    task.archived_at = datetime.utcnow()
    
    # Save billing details
    task.billable_traveling = billable_traveling.strip() if billable_traveling and billable_traveling.strip() else None
    task.billable_labour_onsite = billable_labour_onsite.strip() if billable_labour_onsite and billable_labour_onsite.strip() else None
    task.billable_remote_labour = billable_remote_labour.strip() if billable_remote_labour and billable_remote_labour.strip() else None
    task.billable_equipment_used = billable_equipment_used.strip() if billable_equipment_used and billable_equipment_used.strip() else None
    task.non_billable_traveling = non_billable_traveling.strip() if non_billable_traveling and non_billable_traveling.strip() else None
    task.non_billable_labour_onsite = non_billable_labour_onsite.strip() if non_billable_labour_onsite and non_billable_labour_onsite.strip() else None
    task.non_billable_remote_labour = non_billable_remote_labour.strip() if non_billable_remote_labour and non_billable_remote_labour.strip() else None
    task.non_billable_equipment_used = non_billable_equipment_used.strip() if non_billable_equipment_used and non_billable_equipment_used.strip() else None
    task.completion_notes = completion_notes.strip() if completion_notes and completion_notes.strip() else None
    
    # Add history
    history_entry = TaskHistory(
        task_id=task_id,
        editor_id=user_id,
        field='status',
        old_value=old_status,
        new_value='done'
    )
    db.add(history_entry)
    
    await db.commit()
    
    # Build billing details string for email
    billing_details = []
    
    # Billable items
    billable_items = []
    if task.billable_traveling:
        billable_items.append(f"  - Traveling: {task.billable_traveling}")
    if task.billable_labour_onsite:
        billable_items.append(f"  - Labour Onsite: {task.billable_labour_onsite}")
    if task.billable_remote_labour:
        billable_items.append(f"  - Remote Labour: {task.billable_remote_labour}")
    if task.billable_equipment_used:
        billable_items.append(f"  - Equipment Used: {task.billable_equipment_used}")
    
    if billable_items:
        billing_details.append("BILLABLE:")
        billing_details.extend(billable_items)
    
    # Non-billable items
    non_billable_items = []
    if task.non_billable_traveling:
        non_billable_items.append(f"  - Traveling: {task.non_billable_traveling}")
    if task.non_billable_labour_onsite:
        non_billable_items.append(f"  - Labour Onsite: {task.non_billable_labour_onsite}")
    if task.non_billable_remote_labour:
        non_billable_items.append(f"  - Remote Labour: {task.non_billable_remote_labour}")
    if task.non_billable_equipment_used:
        non_billable_items.append(f"  - Equipment Used: {task.non_billable_equipment_used}")
    
    if non_billable_items:
        if billing_details:
            billing_details.append("")  # Empty line separator
        billing_details.append("NON-BILLABLE:")
        billing_details.extend(non_billable_items)
    
    # Completion notes
    if task.completion_notes:
        if billing_details:
            billing_details.append("")  # Empty line separator
        billing_details.append(f"COMPLETION NOTES:\n{task.completion_notes}")
    
    # Check if this is an AJAX request
    if request.headers.get('accept', '').find('application/json') != -1 or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from fastapi.responses import JSONResponse
        return JSONResponse({
            'success': True, 
            'task_id': task_id,
            'title': task.title,
            'status': 'done'
        })
    
    request.session['success_message'] = f'Task "{task.title}" has been completed.'
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/subtasks')
async def web_task_add_subtasks(
    request: Request,
    task_id: int,
    subtasks: str = Form(...),  # Newline-separated list of subtask titles
    db: AsyncSession = Depends(get_session)
):
    """Add multiple subtasks to a task at once."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get task and verify access
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(
        Task.id == task_id, 
        Project.workspace_id == user.workspace_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Check if task is archived
    if task.is_archived and not user.is_admin:
        raise HTTPException(status_code=403, detail='Cannot add subtasks to archived tasks')
    
    # Check permission: Admin OR assigned to this task
    if not user.is_admin:
        from app.models.assignment import Assignment
        assignment = (await db.execute(
            select(Assignment).where(
                Assignment.task_id == task_id,
                Assignment.assignee_id == user_id
            )
        )).scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=403, detail='You can only add subtasks to tasks assigned to you')
    
    # Get current max order
    from app.models.subtask import Subtask
    max_order_result = await db.execute(
        select(Subtask).where(Subtask.task_id == task_id).order_by(Subtask.order.desc()).limit(1)
    )
    max_order_subtask = max_order_result.scalar_one_or_none()
    current_order = max_order_subtask.order if max_order_subtask else -1
    
    # Parse and create subtasks
    subtask_titles = [title.strip() for title in subtasks.split('\n') if title.strip()]
    
    for title in subtask_titles:
        current_order += 1
        new_subtask = Subtask(
            task_id=task_id,
            title=title,
            is_completed=False,
            order=current_order
        )
        db.add(new_subtask)
    
    await db.commit()
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/subtasks/{subtask_id}/toggle')
async def web_task_toggle_subtask(
    request: Request,
    task_id: int,
    subtask_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Toggle a subtask's completion status."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'error': 'User not found'}, status_code=401)
    
    # Get subtask and verify it belongs to the task
    from app.models.subtask import Subtask
    subtask = (await db.execute(
        select(Subtask).where(Subtask.id == subtask_id, Subtask.task_id == task_id)
    )).scalar_one_or_none()
    
    if not subtask:
        return JSONResponse({'error': 'Subtask not found'}, status_code=404)
    
    # Get task and verify access
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(
        Task.id == task_id,
        Project.workspace_id == user.workspace_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        return JSONResponse({'error': 'Task not found'}, status_code=404)
    
    # Check if task is archived
    if task.is_archived and not user.is_admin:
        return JSONResponse({'error': 'Cannot modify subtasks in archived tasks'}, status_code=403)
    
    # Check permission: Admin OR assigned to this task
    if not user.is_admin:
        from app.models.assignment import Assignment
        assignment = (await db.execute(
            select(Assignment).where(
                Assignment.task_id == task_id,
                Assignment.assignee_id == user_id
            )
        )).scalar_one_or_none()
        if not assignment:
            return JSONResponse({'error': 'Permission denied'}, status_code=403)
    
    # Toggle completion
    from datetime import datetime
    subtask.is_completed = not subtask.is_completed
    subtask.completed_at = datetime.utcnow() if subtask.is_completed else None
    
    await db.commit()
    
    # Calculate completion percentage
    all_subtasks = (await db.execute(
        select(Subtask).where(Subtask.task_id == task_id)
    )).scalars().all()
    
    total = len(all_subtasks)
    completed = sum(1 for st in all_subtasks if st.is_completed)
    percentage = int((completed / total) * 100) if total > 0 else 0
    
    return JSONResponse({
        'success': True,
        'is_completed': subtask.is_completed,
        'completed_at': subtask.completed_at.isoformat() if subtask.completed_at else None,
        'total_subtasks': total,
        'completed_subtasks': completed,
        'completion_percentage': percentage
    })


@router.delete('/tasks/{task_id}/subtasks/{subtask_id}')
async def web_task_delete_subtask(
    request: Request,
    task_id: int,
    subtask_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Delete a subtask."""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'error': 'User not found'}, status_code=401)
    
    # Get subtask and verify it belongs to the task
    from app.models.subtask import Subtask
    subtask = (await db.execute(
        select(Subtask).where(Subtask.id == subtask_id, Subtask.task_id == task_id)
    )).scalar_one_or_none()
    
    if not subtask:
        return JSONResponse({'error': 'Subtask not found'}, status_code=404)
    
    # Get task and verify access
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(
        Task.id == task_id,
        Project.workspace_id == user.workspace_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        return JSONResponse({'error': 'Task not found'}, status_code=404)
    
    # Check if task is archived
    if task.is_archived and not user.is_admin:
        return JSONResponse({'error': 'Cannot delete subtasks from archived tasks'}, status_code=403)
    
    # Check permission: Admin OR assigned to this task
    if not user.is_admin:
        from app.models.assignment import Assignment
        assignment = (await db.execute(
            select(Assignment).where(
                Assignment.task_id == task_id,
                Assignment.assignee_id == user_id
            )
        )).scalar_one_or_none()
        if not assignment:
            return JSONResponse({'error': 'Permission denied'}, status_code=403)
    
    await db.delete(subtask)
    await db.commit()
    
    return JSONResponse({'success': True})


@router.post('/tasks/{task_id}/comment')
async def web_task_add_comment(
    request: Request,
    task_id: int,
    content: str = Form(...),
    files: list[UploadFile] = File(default=[]),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists and belongs to workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Check if task is archived - only admins can comment on archived tasks
    if task.is_archived and not user.is_admin:
        raise HTTPException(status_code=403, detail='This task is archived. Only admins can add comments.')
    
    # Check permission: only admin or assignees can comment
    is_assignee = (await db.execute(
        select(Assignment).where(Assignment.task_id == task_id, Assignment.assignee_id == user_id)
    )).scalar_one_or_none() is not None
    
    if not user.is_admin and not is_assignee:
        raise HTTPException(status_code=403, detail='Only assigned users and admins can comment on this task')
    
    comment = Comment(task_id=task_id, author_id=user_id, content=content)
    db.add(comment)
    await db.flush()  # Get comment.id for attachments
    
    # Notify all assignees except the commenter
    assignees_stmt = (
        select(User)
        .join(Assignment, User.id == Assignment.assignee_id)
        .where(Assignment.task_id == task_id, User.id != user_id)
    )
    assignees = (await db.execute(assignees_stmt)).scalars().all()
    
    commenter_name = user.full_name or user.username
    for assignee in assignees:
        notification = Notification(
            user_id=assignee.id,
            type='comment',
            message=f'{commenter_name} commented on task: {task.title}',
            url=f'/web/tasks/{task_id}'
        )
        db.add(notification)
    
    # Handle file attachments
    if files:
        # Create uploads directory if it doesn't exist
        upload_dir = BASE_DIR / 'uploads' / 'comments'
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            if file.filename:  # Only process if file was actually uploaded
                # Read file content
                file_content = await file.read()
                
                # Validate file size (max 10MB)
                if len(file_content) > 10 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail=f'File {file.filename} is too large. Maximum size is 10MB.')
                
                # Generate unique filename
                file_extension = os.path.splitext(file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = upload_dir / unique_filename
                
                # Save file to disk
                with open(file_path, 'wb') as f:
                    f.write(file_content)
                
                # Store relative path from app directory
                relative_path = f"app/uploads/comments/{unique_filename}"
                
                # Create attachment record
                attachment = CommentAttachment(
                    comment_id=comment.id,
                    filename=file.filename,
                    file_path=relative_path,
                    file_size=len(file_content),
                    content_type=file.content_type or 'application/octet-stream',
                    uploaded_by_id=user_id
                )
                db.add(attachment)
    
    await db.commit()
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/watch')
async def web_task_watch(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Add current user as a watcher of the task."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists and belongs to workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Check if already watching
    from app.models.task_extensions import TaskWatcher
    existing = (await db.execute(
        select(TaskWatcher).where(TaskWatcher.task_id == task_id, TaskWatcher.user_id == user_id)
    )).scalar_one_or_none()
    
    if not existing:
        watcher = TaskWatcher(task_id=task_id, user_id=user_id)
        db.add(watcher)
        await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/unwatch')
async def web_task_unwatch(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Remove current user as a watcher of the task."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists and belongs to workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Remove watcher
    from app.models.task_extensions import TaskWatcher
    existing = (await db.execute(
        select(TaskWatcher).where(TaskWatcher.task_id == task_id, TaskWatcher.user_id == user_id)
    )).scalar_one_or_none()
    
    if existing:
        await db.delete(existing)
        await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/dependencies/add')
async def web_task_add_dependency(
    request: Request,
    task_id: int,
    blocker_task_id: int = Form(...),
    db: AsyncSession = Depends(get_session)
):
    """Add a blocking dependency to the task."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists and belongs to workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Verify blocker task exists and belongs to same project
    blocker = (await db.execute(
        select(Task).where(Task.id == blocker_task_id, Task.project_id == task.project_id)
    )).scalar_one_or_none()
    if not blocker:
        raise HTTPException(status_code=404, detail='Blocker task not found')
    
    # Check for circular dependencies (simple check)
    if blocker_task_id == task_id:
        raise HTTPException(status_code=400, detail='Task cannot block itself')
    
    # Check if dependency already exists
    from app.models.task_extensions import TaskDependency
    existing = (await db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task_id, 
            TaskDependency.depends_on_task_id == blocker_task_id
        )
    )).scalar_one_or_none()
    
    if not existing:
        dependency = TaskDependency(
            task_id=task_id, 
            depends_on_task_id=blocker_task_id,
            created_by_id=user_id
        )
        db.add(dependency)
        await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.post('/tasks/{task_id}/dependencies/{dep_task_id}/remove')
async def web_task_remove_dependency(
    request: Request,
    task_id: int,
    dep_task_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Remove a blocking dependency from the task."""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify task exists and belongs to workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Remove dependency
    from app.models.task_extensions import TaskDependency
    existing = (await db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task_id,
            TaskDependency.depends_on_task_id == dep_task_id
        )
    )).scalar_one_or_none()
    
    if existing:
        await db.delete(existing)
        await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


@router.get('/attachments/{attachment_id}/preview')
async def preview_comment_attachment(
    request: Request,
    attachment_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get attachment with permission check
    attachment = (await db.execute(
        select(CommentAttachment)
        .join(Comment, CommentAttachment.comment_id == Comment.id)
        .join(Task, Comment.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(
            CommentAttachment.id == attachment_id,
            Project.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(status_code=404, detail='Attachment not found')
    
    # Handle both absolute paths (old) and relative paths (new)
    file_path = Path(attachment.file_path)
    logger.debug(f"Attachment file_path from DB: {attachment.file_path}")
    logger.debug(f"Is absolute: {file_path.is_absolute()}")
    
    if not file_path.is_absolute():
        # Relative path - resolve from current working directory
        file_path = Path.cwd() / file_path
    
    logger.debug(f"Resolved file_path: {file_path}")
    logger.debug(f"File exists: {file_path.exists()}")
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail=f'File not found on disk: {file_path}')
    
    # Serve file inline for preview with proper headers for PDF embedding
    return FileResponse(
        path=str(file_path),
        media_type=attachment.content_type,
        filename=attachment.filename,
        headers={
            'Content-Disposition': f'inline; filename="{attachment.filename}"',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': "frame-ancestors 'self'"
        }
    )


@router.get('/attachments/{attachment_id}/download')
async def download_comment_attachment(
    request: Request,
    attachment_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get attachment with permission check
    attachment = (await db.execute(
        select(CommentAttachment)
        .join(Comment, CommentAttachment.comment_id == Comment.id)
        .join(Task, Comment.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(
            CommentAttachment.id == attachment_id,
            Project.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(status_code=404, detail='Attachment not found')
    
    # Handle both absolute paths (old) and relative paths (new)
    file_path = Path(attachment.file_path)
    if not file_path.is_absolute():
        # Relative path - resolve from current working directory
        file_path = Path.cwd() / file_path
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail='File not found on disk')
    
    return FileResponse(
        path=str(file_path),
        filename=attachment.filename,
        media_type=attachment.content_type
    )


@router.post('/attachments/{attachment_id}/delete')
async def delete_comment_attachment(
    request: Request,
    attachment_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Delete a comment attachment"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse(status_code=401, content={'detail': 'Not authenticated'})
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse(status_code=401, content={'detail': 'User not found'})
    
    # Get attachment with permission check
    attachment = (await db.execute(
        select(CommentAttachment)
        .join(Comment, CommentAttachment.comment_id == Comment.id)
        .join(Task, Comment.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(
            CommentAttachment.id == attachment_id,
            Project.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not attachment:
        return JSONResponse(status_code=404, content={'detail': 'Attachment not found'})
    
    # Check permission - only admin or the comment author can delete
    comment = (await db.execute(select(Comment).where(Comment.id == attachment.comment_id))).scalar_one_or_none()
    if not user.is_admin and (not comment or comment.user_id != user.id):
        return JSONResponse(status_code=403, content={'detail': 'Permission denied'})
    
    # Delete file from disk
    file_path = Path(attachment.file_path)
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path
    
    if file_path.exists():
        try:
            file_path.unlink()
        except Exception as e:
            pass  # File may already be deleted
    
    # Delete from database
    await db.delete(attachment)
    await db.commit()
    
    return JSONResponse(status_code=200, content={'success': True})


@router.post('/tasks/{task_id}/status')
async def web_task_update_status(request: Request, task_id: int, status_value: str = Form(...), db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    # Ensure task belongs to user's workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Check permission: Admin OR project member
    if not user.is_admin:
        from app.models.project_member import ProjectMember
        member = (await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == user_id
            )
        )).scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=403, detail='You must be a project member to update tasks')
    
    if status_value not in [s.value for s in TaskStatus]:
        raise HTTPException(status_code=400, detail='Invalid status')
    
    # Track change
    old_status = task.status.value
    task.status = TaskStatus(status_value)
    
    # Auto-archive when moved to done
    if status_value == 'done':
        task.is_archived = True
        task.archived_at = datetime.utcnow()
    elif old_status == 'done' and status_value != 'done':
        # Unarchive if moved out of done
        task.is_archived = False
        task.archived_at = None
    
    # Save history
    history_entry = TaskHistory(
        task_id=task_id,
        editor_id=user_id,
        field='status',
        old_value=old_status,
        new_value=status_value
    )
    db.add(history_entry)
    
    await db.commit()
    
    # Check if this is an AJAX request (fetch)
    if request.headers.get('accept', '').find('application/json') != -1 or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from fastapi.responses import JSONResponse
        return JSONResponse({'success': True, 'status': status_value})
    
    return RedirectResponse(f'/web/projects/{task.project_id}', status_code=303)


@router.post('/tasks/{task_id}/assign')
async def web_task_assign(request: Request, task_id: int, assignee_id: int = Form(...), db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can assign tasks to users
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Only admins can assign tasks')
    
    # Ensure task belongs to user's workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    # Verify assignee is in same workspace and is active
    assignee = (await db.execute(select(User).where(User.id == assignee_id, User.workspace_id == user.workspace_id, User.is_active == True))).scalar_one_or_none()
    if not assignee:
        raise HTTPException(status_code=400, detail='Invalid assignee or user is inactive')
    # Check if already assigned
    existing = (await db.execute(select(Assignment).where(Assignment.task_id == task_id, Assignment.assignee_id == assignee_id))).scalar_one_or_none()
    if not existing:
        assignment = Assignment(task_id=task_id, assignee_id=assignee_id)
        db.add(assignment)
        
        # Create notification for the assignee (don't notify if assigning to self)
        if assignee_id != user_id:
            assigner = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
            assigner_name = assigner.full_name or assigner.username if assigner else "Someone"
            
            notification = Notification(
                user_id=assignee_id,
                type='task_assigned',
                message=f'{assigner_name} assigned you to task: {task.title}',
                url=f'/web/tasks/{task_id}'
            )
            db.add(notification)
        
        await db.commit()
    return RedirectResponse(f'/web/projects/{task.project_id}', status_code=303)


@router.post('/tasks/{task_id}/unassign')
async def web_task_unassign(request: Request, task_id: int, assignee_id: int = Form(...), db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can unassign tasks
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Only admins can unassign tasks')
    
    # Ensure task belongs to user's workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    # Delete assignment
    assignment = (await db.execute(select(Assignment).where(Assignment.task_id == task_id, Assignment.assignee_id == assignee_id))).scalar_one_or_none()
    if assignment:
        await db.delete(assignment)
        await db.commit()
    return RedirectResponse(f'/web/projects/{task.project_id}', status_code=303)


@router.post('/tasks/{task_id}/delete')
async def web_task_delete(request: Request, task_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can delete tasks
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Only admins can delete tasks')
    
    # Ensure task belongs to user's workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    project_id = task.project_id
    
    # Delete the task (cascade will handle assignments, comments, etc.)
    await db.delete(task)
    await db.commit()
    
    return RedirectResponse(f'/web/projects/{project_id}', status_code=303)


@router.post('/tasks/{task_id}/reopen')
async def web_task_reopen(request: Request, task_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can reopen tasks
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Only admins can reopen tasks')
    
    # Ensure task belongs to user's workspace
    stmt = select(Task).join(Project, Task.project_id == Project.id).where(Task.id == task_id, Project.workspace_id == user.workspace_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    # Reopen the task
    task.is_archived = False
    task.archived_at = None
    # If status is done, set it back to in_progress
    if task.status == TaskStatus.done:
        task.status = TaskStatus.in_progress
    
    await db.commit()
    
    return RedirectResponse(f'/web/tasks/{task_id}', status_code=303)


# Meetings
@router.get('/meetings')
async def web_meetings_list(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get all meetings where user is an attendee or organizer
    stmt = (
        select(Meeting)
        .join(MeetingAttendee, Meeting.id == MeetingAttendee.meeting_id)
        .where(MeetingAttendee.user_id == user_id)
        .order_by(Meeting.start_time.desc())
    )
    result = await db.execute(stmt)
    meetings = result.scalars().all()
    
    # Get all active workspace users for the create form
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id, User.is_active == True)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    return templates.TemplateResponse('meetings/list.html', {
        'request': request,
        'meetings': meetings,
        'users': users,
        'user': user
    })


@router.post('/meetings/create')
async def web_meeting_create(
    request: Request,
    title: str = Form(...),
    start_time_str: str = Form(..., alias='start_time'),
    end_time_str: str = Form(..., alias='end_time'),
    platform: str = Form(...),
    meeting_url: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    auto_generate_meet: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Parse datetime strings
    from datetime import datetime
    try:
        start_datetime = datetime.fromisoformat(start_time_str)
        end_datetime = datetime.fromisoformat(end_time_str)
        
        # Extract date and time components
        meeting_date = start_datetime.date()
        meeting_time = start_datetime.time()
        
        # Calculate duration in minutes
        duration = int((end_datetime - start_datetime).total_seconds() / 60)
        if duration <= 0:
            # Return user to form with error message instead of HTTP exception
            from fastapi.responses import HTMLResponse
            from fastapi.templating import Jinja2Templates
            templates = Jinja2Templates(directory="app/templates")
            
            # Get users for the form
            users_result = await db.execute(
                select(User).where(User.workspace_id == user.workspace_id).order_by(User.full_name)
            )
            users = users_result.scalars().all()
            
            return templates.TemplateResponse("meetings/list.html", {
                "request": request,
                "user": user,
                "meetings": [],
                "users": users,
                "error": "End time must be after start time. Please select a later end time."
            })
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Invalid datetime format: {str(e)}')
    
    # Auto-generate Google Meet link if requested
    generated_meet_url = None
    if auto_generate_meet == 'on' and platform == 'google_meet' and user.google_access_token:
        try:
            from app.core.google_oauth import create_calendar_event
            
            # Get attendee emails
            form_data = await request.form()
            attendee_ids = form_data.getlist('attendee_ids')
            attendee_emails = []
            
            if attendee_ids:
                attendees_result = await db.execute(
                    select(User).where(User.id.in_([int(aid) for aid in attendee_ids]))
                )
                attendees = attendees_result.scalars().all()
                attendee_emails = [a.email for a in attendees if a.email]
            
            # Create Google Calendar event with Meet link
            calendar_event = create_calendar_event(
                access_token=user.google_access_token,
                refresh_token=user.google_refresh_token,
                token_expiry=user.google_token_expiry,
                summary=title,
                description=description or '',
                start_time=start_datetime,
                end_time=end_datetime,
                attendees=attendee_emails,
                add_google_meet=True
            )
            
            if calendar_event and 'hangoutLink' in calendar_event:
                generated_meet_url = calendar_event['hangoutLink']
                meeting_url = generated_meet_url
                logger.info(f"Auto-generated Google Meet link: {generated_meet_url}")
            else:
                logger.warning("Failed to generate Google Meet link - no hangoutLink in response")
                
        except Exception as e:
            logger.error(f"Error auto-generating Google Meet link: {e}")
            # Continue with meeting creation without the auto-generated link
    
    # Create meeting
    meeting = Meeting(
        title=title,
        description=description,
        date=meeting_date,
        start_time=meeting_time,
        duration_minutes=duration,
        platform=MeetingPlatform(platform),
        url=meeting_url,
        organizer_id=user_id,
        workspace_id=user.workspace_id
    )
    db.add(meeting)
    await db.flush()  # Get the meeting ID
    
    # Add organizer as attendee
    attendee = MeetingAttendee(meeting_id=meeting.id, user_id=user_id)
    db.add(attendee)
    
    # Get attendee IDs from form (if provided)
    form_data = await request.form()
    attendee_ids = form_data.getlist('attendee_ids')
    for attendee_id in attendee_ids:
        if int(attendee_id) != user_id:  # Don't duplicate organizer
            attendee = MeetingAttendee(meeting_id=meeting.id, user_id=int(attendee_id))
            db.add(attendee)
    
    await db.commit()
    return RedirectResponse('/web/meetings', status_code=303)


@router.post('/meetings/{meeting_id}/cancel')
async def web_meeting_cancel(
    request: Request,
    meeting_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get the meeting
    meeting = (await db.execute(select(Meeting).where(Meeting.id == meeting_id))).scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found')
    
    # Check if user has permission (organizer or admin)
    if meeting.organizer_id != user_id and not user.is_admin:
        raise HTTPException(status_code=403, detail='Not authorized to cancel this meeting')
    
    # Check if already cancelled
    if meeting.is_cancelled:
        return RedirectResponse('/web/meetings', status_code=303)
    
    # Cancel the meeting
    from datetime import datetime
    meeting.is_cancelled = True
    meeting.cancelled_at = datetime.utcnow()
    meeting.cancelled_by = user_id
    
    await db.commit()
    return RedirectResponse('/web/meetings', status_code=303)


@router.get('/meetings/{meeting_id}/details')
async def web_meeting_details(
    request: Request,
    meeting_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Get meeting details for display in modal"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JSONResponse({'error': 'Not authenticated'}, status_code=401)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return JSONResponse({'error': 'User not found'}, status_code=401)
    
    # Get the meeting
    meeting = (await db.execute(select(Meeting).where(Meeting.id == meeting_id))).scalar_one_or_none()
    if not meeting:
        return JSONResponse({'error': 'Meeting not found'}, status_code=404)
    
    # Check if user has access to this meeting (is attendee, organizer, or admin)
    is_organizer = meeting.organizer_id == user_id
    attendee = (await db.execute(
        select(MeetingAttendee).where(
            MeetingAttendee.meeting_id == meeting_id,
            MeetingAttendee.user_id == user_id
        )
    )).scalar_one_or_none()
    
    if not (is_organizer or attendee or user.is_admin):
        return JSONResponse({'error': 'Not authorized to view this meeting'}, status_code=403)
    
    # Get organizer details
    organizer = (await db.execute(select(User).where(User.id == meeting.organizer_id))).scalar_one_or_none()
    
    # Get all attendees
    attendees_data = (await db.execute(
        select(MeetingAttendee, User)
        .join(User, MeetingAttendee.user_id == User.id)
        .where(MeetingAttendee.meeting_id == meeting_id)
    )).all()
    
    # Get cancelled by user if meeting is cancelled
    cancelled_by_user = None
    if meeting.is_cancelled and meeting.cancelled_by:
        cancelled_by_user = (await db.execute(
            select(User).where(User.id == meeting.cancelled_by)
        )).scalar_one_or_none()
    
    return JSONResponse({
        'id': meeting.id,
        'title': meeting.title,
        'description': meeting.description,
        'date': meeting.date.strftime('%d/%m/%Y'),
        'date_formatted': meeting.date.strftime('%d/%m/%Y'),
        'start_time': meeting.start_time.strftime('%I:%M %p'),
        'duration_minutes': meeting.duration_minutes,
        'platform': meeting.platform.value,
        'platform_display': meeting.platform.value.replace('_', ' ').title(),
        'url': meeting.url,
        'organizer': {
            'id': organizer.id if organizer else None,
            'name': organizer.full_name if organizer else 'Unknown',
            'email': organizer.email if organizer else ''
        },
        'attendees': [
            {
                'id': user_obj.id,
                'name': user_obj.full_name,
                'email': user_obj.email,
                'status': attendee_obj.status or 'invited'
            }
            for attendee_obj, user_obj in attendees_data
        ],
        'is_cancelled': meeting.is_cancelled,
        'cancelled_at': meeting.cancelled_at.strftime('%d/%m/%Y at %I:%M %p') if meeting.cancelled_at else None,
        'cancelled_by': cancelled_by_user.full_name if cancelled_by_user else None,
        'is_organizer': is_organizer,
        'is_admin': user.is_admin
    })


# Calendar
@router.get('/calendar')
async def web_calendar(
    request: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    view: str = 'month',
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Default to current date if not specified
    today = date.today()
    year = year or today.year
    month = month or today.month
    day = day or today.day
    
    # Calculate prev/next month for navigation
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    # Determine date range based on view
    if view == 'day':
        current_date = date(year, month, day)
        first_day = current_date
        last_day = current_date
        weeks = []
    elif view == 'week':
        current_date = date(year, month, day)
        # Get Monday of current week
        start_of_week = current_date - timedelta(days=current_date.weekday())
        first_day = start_of_week
        last_day = start_of_week + timedelta(days=6)
        weeks = [[start_of_week + timedelta(days=i) for i in range(7)]]
    else:  # month view
        current_date = date(year, month, day)
        # Build calendar weeks with date objects
        cal = pycalendar.Calendar(firstweekday=0)  # Monday first
        weeks = []
        for week in cal.monthdatescalendar(year, month):
            weeks.append(week)
        # Get all tasks with due dates for display (include adjacent months shown in calendar)
        first_day = weeks[0][0]
        last_day = weeks[-1][-1]
    
    # Admin sees all tasks, regular users see only their assigned tasks
    # Fetch tasks that overlap with the calendar view period (either by start_date or due_date)
    if user.is_admin:
        stmt = (
            select(Task)
            .join(Project, Task.project_id == Project.id)
            .where(
                Project.workspace_id == user.workspace_id,
                # Task has at least a due_date or start_date
                (Task.due_date.isnot(None)) | (Task.start_date.isnot(None)),
                # Task overlaps with calendar period
                (
                    # Tasks with both start and due dates - check if they overlap calendar period
                    ((Task.start_date.isnot(None)) & (Task.due_date.isnot(None)) & 
                     (Task.start_date <= last_day) & (Task.due_date >= first_day)) |
                    # Tasks with only due_date - check if in period
                    ((Task.start_date.is_(None)) & (Task.due_date.isnot(None)) & 
                     (Task.due_date >= first_day) & (Task.due_date <= last_day)) |
                    # Tasks with only start_date - check if in period
                    ((Task.start_date.isnot(None)) & (Task.due_date.is_(None)) & 
                     (Task.start_date >= first_day) & (Task.start_date <= last_day))
                )
            )
            .order_by(Task.start_date, Task.due_date, Task.due_time)
        )
    else:
        stmt = (
            select(Task)
            .join(Project, Task.project_id == Project.id)
            .join(Assignment, Task.id == Assignment.task_id)
            .where(
                Project.workspace_id == user.workspace_id,
                Assignment.assignee_id == user.id,
                # Task has at least a due_date or start_date
                (Task.due_date.isnot(None)) | (Task.start_date.isnot(None)),
                # Task overlaps with calendar period
                (
                    # Tasks with both start and due dates - check if they overlap calendar period
                    ((Task.start_date.isnot(None)) & (Task.due_date.isnot(None)) & 
                     (Task.start_date <= last_day) & (Task.due_date >= first_day)) |
                    # Tasks with only due_date - check if in period
                    ((Task.start_date.is_(None)) & (Task.due_date.isnot(None)) & 
                     (Task.due_date >= first_day) & (Task.due_date <= last_day)) |
                    # Tasks with only start_date - check if in period
                    ((Task.start_date.isnot(None)) & (Task.due_date.is_(None)) & 
                     (Task.start_date >= first_day) & (Task.start_date <= last_day))
                )
            )
            .order_by(Task.start_date, Task.due_date, Task.due_time)
        )
    tasks = (await db.execute(stmt)).scalars().all()
    
    # Fetch projects with date ranges for calendar display
    # Admin sees all projects, regular users see projects they're assigned to (via tasks or project_member)
    from app.models.project_member import ProjectMember
    
    if user.is_admin:
        projects_stmt = (
            select(Project)
            .where(
                Project.workspace_id == user.workspace_id,
                Project.start_date.isnot(None),
                Project.due_date.isnot(None),
                Project.is_archived == False,
                # Project overlaps with calendar view period
                Project.start_date <= last_day,
                Project.due_date >= first_day
            )
            .order_by(Project.start_date)
        )
    else:
        # Get projects where user is a member or has assigned tasks
        projects_stmt = (
            select(Project)
            .join(ProjectMember, Project.id == ProjectMember.project_id)
            .where(
                Project.workspace_id == user.workspace_id,
                ProjectMember.user_id == user.id,
                Project.start_date.isnot(None),
                Project.due_date.isnot(None),
                Project.is_archived == False,
                Project.start_date <= last_day,
                Project.due_date >= first_day
            )
            .distinct()
            .order_by(Project.start_date)
        )
    projects = (await db.execute(projects_stmt)).scalars().all()
    
    # Sort tasks by priority (critical, high, medium, low)
    # Use date.max for None due_dates to put them at the end
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    
    def task_sort_key(t):
        due = t.due_date if t.due_date else date.max
        priority_val = t.priority.value if t.priority else 'low'
        priority = priority_order.get(priority_val, 4)
        due_time = t.due_time if t.due_time else time.max
        return (due, priority, due_time)
    
    tasks = sorted(tasks, key=task_sort_key)
    
    # Get meetings for the calendar period
    # Admin sees all meetings, regular users see only meetings they're attending
    if user.is_admin:
        meetings_stmt = (
            select(Meeting)
            .where(
                Meeting.workspace_id == user.workspace_id,
                Meeting.date >= first_day,
                Meeting.date <= last_day
            )
            .order_by(Meeting.date, Meeting.start_time)
        )
    else:
        meetings_stmt = (
            select(Meeting)
            .join(MeetingAttendee, Meeting.id == MeetingAttendee.meeting_id)
            .where(
                Meeting.workspace_id == user.workspace_id,
                MeetingAttendee.user_id == user.id,
                Meeting.date >= first_day,
                Meeting.date <= last_day
            )
            .order_by(Meeting.date, Meeting.start_time)
        )
    meetings = (await db.execute(meetings_stmt)).scalars().all()
    
    # Get all workspace users for color legend (admin view)
    workspace_users = []
    if user.is_admin:
        workspace_users_stmt = (
            select(User)
            .where(
                User.workspace_id == user.workspace_id,
                User.is_active == True
            )
            .order_by(User.full_name)
        )
        workspace_users = (await db.execute(workspace_users_stmt)).scalars().all()
    
    # Build a map of task/project IDs to their assigned users for color coding
    task_users = {}
    for task in tasks:
        # Get all users assigned to this task
        task_assignments = (await db.execute(
            select(User)
            .join(Assignment, User.id == Assignment.assignee_id)
            .where(Assignment.task_id == task.id)
        )).scalars().all()
        if task_assignments:
            task_users[task.id] = list(task_assignments)  # Store all assigned users
    
    project_users = {}
    for project in projects:
        # Get project owner for color coding
        project_owner = (await db.execute(
            select(User).where(User.id == project.owner_id)
        )).scalar_one_or_none()
        if project_owner:
            project_users[project.id] = project_owner
    
    # Calculate navigation dates based on view
    if view == 'day':
        prev_date = current_date - timedelta(days=1)
        next_date = current_date + timedelta(days=1)
        prev_year, prev_month, prev_day = prev_date.year, prev_date.month, prev_date.day
        next_year, next_month, next_day = next_date.year, next_date.month, next_date.day
    elif view == 'week':
        prev_week_start = first_day - timedelta(days=7)
        next_week_start = first_day + timedelta(days=7)
        prev_year, prev_month, prev_day = prev_week_start.year, prev_week_start.month, prev_week_start.day
        next_year, next_month, next_day = next_week_start.year, next_week_start.month, next_week_start.day
    else:  # month
        prev_day = 1
        next_day = 1
    
    return templates.TemplateResponse('calendar/index.html', {
        'request': request,
        'user': user,
        'view': view,
        'year': year,
        'month': month,
        'day': day,
        'current_date': current_date,
        'first_day': first_day,
        'last_day': last_day,
        'weeks': weeks,
        'tasks': tasks,
        'meetings': meetings,
        'projects': projects,
        'task_users': task_users,
        'project_users': project_users,
        'workspace_users': workspace_users,
        'today': today,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'prev_day': prev_day,
        'next_month': next_month,
        'next_year': next_year,
        'next_day': next_day,
        'TaskStatus': TaskStatus
    })


# Chats
@router.get('/chats')
async def web_chats_list(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get all chats where user is a member
    stmt = (
        select(Chat)
        .join(ChatMember, Chat.id == ChatMember.chat_id)
        .where(ChatMember.user_id == user_id)
        .order_by(Chat.created_at.desc())
    )
    chats = (await db.execute(stmt)).scalars().all()
    
    # Get all active workspace users for creating new chats
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id, User.id != user_id, User.is_active == True)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    return templates.TemplateResponse('chats/list.html', {
        'request': request,
        'chats': chats,
        'users': users,
        'user': user
    })


@router.post('/chats/create')
async def web_chat_create(
    request: Request,
    name: Optional[str] = Form(None),
    is_group: bool = Form(False),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Create chat
    chat = Chat(
        name=name,
        is_group=is_group,
        workspace_id=user.workspace_id,
        created_by_id=user_id  # Set the creator
    )
    db.add(chat)
    await db.flush()
    
    # Add creator as member
    member = ChatMember(chat_id=chat.id, user_id=user_id)
    db.add(member)
    
    # Add selected members
    form_data = await request.form()
    member_ids = form_data.getlist('member_ids')
    for member_id in member_ids:
        if int(member_id) != user_id:
            member = ChatMember(chat_id=chat.id, user_id=int(member_id))
            db.add(member)
    
    await db.commit()
    return RedirectResponse(f'/web/chats/{chat.id}', status_code=303)


@router.get('/chats/{chat_id}')
async def web_chat_detail(request: Request, chat_id: int, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify user is member of this chat
    membership = (await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
    )).scalar_one_or_none()
    
    if not membership:
        raise HTTPException(status_code=403, detail='Not a member of this chat')
    
    # Get chat details
    chat = (await db.execute(select(Chat).where(Chat.id == chat_id))).scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail='Chat not found')
    
    # Get all messages
    messages_stmt = (
        select(Message, User.full_name, User.email)
        .join(User, Message.author_id == User.id)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
    )
    results = (await db.execute(messages_stmt)).all()
    
    # Get attachments for all messages
    from app.models.chat import MessageAttachment
    message_ids = [msg.id for msg, _, _ in results]
    attachments_stmt = (
        select(MessageAttachment)
        .where(MessageAttachment.message_id.in_(message_ids) if message_ids else False)
        .order_by(MessageAttachment.uploaded_at.asc())
    )
    all_attachments = (await db.execute(attachments_stmt)).scalars().all()
    
    # Group attachments by message_id
    attachments_by_message = {}
    for att in all_attachments:
        attachments_by_message.setdefault(att.message_id, []).append(att)
    
    # Combine messages with sender names and attachments
    messages_with_sender = [
        (msg, full_name or email, attachments_by_message.get(msg.id, []))
        for msg, full_name, email in results
    ]
    
    # Get chat members
    members_stmt = (
        select(User)
        .join(ChatMember, User.id == ChatMember.user_id)
        .where(ChatMember.chat_id == chat_id)
        .order_by(User.full_name, User.email)
    )
    members = (await db.execute(members_stmt)).scalars().all()
    
    return templates.TemplateResponse('chats/detail.html', {
        'request': request,
        'chat': chat,
        'messages': messages_with_sender,
        'members': members,
        'user': user
    })


@router.get('/chats/attachments/{attachment_id}/download')
async def download_chat_attachment(
    request: Request,
    attachment_id: int,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    from app.models.chat import MessageAttachment
    from fastapi.responses import FileResponse
    import os
    
    # Get attachment
    attachment = (await db.execute(
        select(MessageAttachment).where(MessageAttachment.id == attachment_id)
    )).scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(status_code=404, detail='Attachment not found')
    
    # Verify user has access to this chat
    message = (await db.execute(select(Message).where(Message.id == attachment.message_id))).scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail='Message not found')
    
    membership = (await db.execute(
        select(ChatMember).where(
            ChatMember.chat_id == message.chat_id,
            ChatMember.user_id == user_id
        )
    )).scalar_one_or_none()
    
    if not membership:
        raise HTTPException(status_code=403, detail='Access denied')
    
    # Handle both absolute paths (old) and relative paths (new)
    file_path = Path(attachment.file_path)
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail='File not found on disk')
    
    return FileResponse(
        path=str(file_path),
        filename=attachment.filename,
        media_type=attachment.mime_type or 'application/octet-stream'
    )


@router.post('/chats/{chat_id}/messages')
async def web_chat_send_message(
    request: Request,
    chat_id: int,
    content: Optional[str] = Form(None),
    attachments: Optional[list[UploadFile]] = File(None),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Verify membership
    membership = (await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
    )).scalar_one_or_none()
    
    if not membership:
        raise HTTPException(status_code=403, detail='Not a member of this chat')
    
    # Require either content or attachments
    if not content and not attachments:
        return RedirectResponse(f'/web/chats/{chat_id}', status_code=303)
    
    # Create message
    message = Message(
        chat_id=chat_id,
        author_id=user_id,
        content=content or ""
    )
    db.add(message)
    await db.flush()  # Get message ID
    
    # Handle file attachments
    if attachments:
        import uuid
        from pathlib import Path
        
        upload_dir = Path('app/uploads/chat_messages')
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in attachments:
            if file.filename:
                # Read file content first for validation
                content_bytes = await file.read()
                
                # Validate file size (max 10MB)
                if len(content_bytes) > 10 * 1024 * 1024:
                    continue  # Skip files that are too large
                
                # Block dangerous file extensions
                file_ext = Path(file.filename).suffix.lower()
                blocked_extensions = {'.exe', '.bat', '.cmd', '.sh', '.php', '.py', '.rb', '.pl', '.cgi', '.js', '.msi', '.ps1', '.vbs', '.wsf'}
                if file_ext in blocked_extensions:
                    continue  # Skip dangerous file types
                
                # Generate unique filename
                unique_filename = f"{uuid.uuid4()}{file_ext}"
                file_path = upload_dir / unique_filename
                
                # Save file
                with open(file_path, 'wb') as f:
                    f.write(content_bytes)
                
                # Create attachment record
                from app.models.chat import MessageAttachment
                attachment = MessageAttachment(
                    message_id=message.id,
                    filename=file.filename,
                    file_path=str(file_path),
                    file_size=len(content_bytes),
                    mime_type=file.content_type
                )
                db.add(attachment)
    
    # Create notifications for other chat members
    chat_members = (await db.execute(
        select(ChatMember)
        .where(ChatMember.chat_id == chat_id, ChatMember.user_id != user_id)
    )).scalars().all()
    
    # Get chat info for notification message
    chat = (await db.execute(select(Chat).where(Chat.id == chat_id))).scalar_one_or_none()
    
    # Build intelligent notification message
    chat_name = chat.name if chat and chat.name else 'chat'
    sender_name = user.full_name or user.username
    
    # Create message preview (keep it short)
    message_preview = ""
    if content:
        # Truncate long messages
        preview_text = content.strip()
        if len(preview_text) > 50:
            preview_text = preview_text[:47] + "..."
        message_preview = f": {preview_text}"
    
    # Check for attachments and add to summary
    attachment_summary = ""
    if attachments and len(attachments) > 0:
        attachment_count = len(attachments)
        
        # Analyze attachment types
        image_count = sum(1 for f in attachments if f.content_type and f.content_type.startswith('image/'))
        video_count = sum(1 for f in attachments if f.content_type and f.content_type.startswith('video/'))
        doc_count = sum(1 for f in attachments if f.content_type and (
            'pdf' in (f.content_type or '') or 
            'document' in (f.content_type or '') or
            'word' in (f.content_type or '') or
            'sheet' in (f.content_type or '') or
            'text' in (f.content_type or '')
        ))
        
        # Build attachment description
        attachment_parts = []
        if image_count > 0:
            attachment_parts.append(f"{image_count} image{'s' if image_count > 1 else ''}")
        if video_count > 0:
            attachment_parts.append(f"{video_count} video{'s' if video_count > 1 else ''}")
        if doc_count > 0:
            attachment_parts.append(f"{doc_count} document{'s' if doc_count > 1 else ''}")
        
        # If there are other files not categorized
        other_count = attachment_count - (image_count + video_count + doc_count)
        if other_count > 0:
            attachment_parts.append(f"{other_count} file{'s' if other_count > 1 else ''}")
        
        if attachment_parts:
            attachment_summary = f" [{', '.join(attachment_parts)}]"
        else:
            attachment_summary = f" [{attachment_count} attachment{'s' if attachment_count > 1 else ''}]"
    
    # Combine everything into a concise notification
    if message_preview and attachment_summary:
        notification_text = f"{sender_name}{message_preview} {attachment_summary}"
    elif attachment_summary:
        notification_text = f"{sender_name} sent {attachment_summary.strip('[]')} in {chat_name}"
    elif message_preview:
        notification_text = f"{sender_name} in {chat_name}{message_preview}"
    else:
        notification_text = f"{sender_name} sent a message in {chat_name}"
    
    for member in chat_members:
        # Create notification for each member
        notification = Notification(
            user_id=member.user_id,
            type='message',
            message=notification_text,
            url=f'/web/chats/{chat_id}',
            related_id=message.id
        )
        db.add(notification)
    
    await db.commit()
    
    return RedirectResponse(f'/web/chats/{chat_id}', status_code=303)


# Invite Users
@router.get('/users/new')
async def web_invite_user_form(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Get current workspace users
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    return templates.TemplateResponse('users/invite.html', {
        'request': request,
        'users': users,
        'user': user,
        'error': None,
        'success': None
    })


@router.post('/users/invite')
async def web_invite_user(
    request: Request,
    email: str = Form(...),
    full_name: Optional[str] = Form(None),
    is_admin: bool = Form(False),
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    # Only admins can invite users
    if not user.is_admin:
        return RedirectResponse('/web/dashboard', status_code=303)
    
    # Check if user with email already exists
    existing = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    if existing:
        return templates.TemplateResponse('users/invite.html', {
            'request': request,
            'users': users,
            'user': user,
            'error': 'User with this email already exists',
            'success': None
        }, status_code=400)
    
    # Create new user in the same workspace with a temporary password
    import secrets
    temp_password = secrets.token_urlsafe(16)
    
    # Generate username from email (before @ symbol)
    username_base = email.split('@')[0].lower()
    # Check if username exists, add number if needed
    username = username_base
    counter = 1
    while True:
        existing_username = (await db.execute(
            select(User).where(User.username == username)
        )).scalar_one_or_none()
        if not existing_username:
            break
        username = f"{username_base}{counter}"
        counter += 1
    
    new_user = User(
        username=username,
        email=email,
        full_name=full_name or '',
        hashed_password=get_password_hash(temp_password),
        workspace_id=user.workspace_id,
        is_admin=is_admin,
        email_verified=True,  # OTP disabled
        profile_completed=True  # Skip profile completion for invited users
    )
    db.add(new_user)
    await db.commit()
    
    # In a real app, you'd send an email with the temp password or invitation link
    # For now, we'll just show a success message
    users = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id)
        .order_by(User.full_name, User.email)
    )).scalars().all()
    
    return templates.TemplateResponse('users/invite.html', {
        'request': request,
        'users': users,
        'user': user,
        'error': None,
        'success': f'User invited successfully! Username: {username}, Temporary password: {temp_password} (share these securely)'
    })


@router.post('/users/{user_id}/delete')
async def web_delete_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return RedirectResponse('/web/login', status_code=303)
    current_user = (await db.execute(select(User).where(User.id == current_user_id))).scalar_one_or_none()
    if not current_user or not current_user.is_admin:
        return RedirectResponse('/web/projects', status_code=303)
    
    # Get user to delete
    user_to_delete = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user_to_delete or user_to_delete.workspace_id != current_user.workspace_id:
        return RedirectResponse('/web/users/new', status_code=303)
    
    # Prevent deleting yourself
    if user_to_delete.id == current_user.id:
        return RedirectResponse('/web/users/new', status_code=303)
    
    # Deactivate user instead of deleting (preserves audit trail)
    user_to_delete.is_active = False
    await db.commit()
    
    return RedirectResponse('/web/users/new', status_code=303)


@router.get('/set-password')
async def web_set_password_form(request: Request, token: Optional[str] = None):
    return templates.TemplateResponse('auth/set_password.html', {
        'request': request,
        'token': token,
        'error': None
    })


@router.post('/set-password')
async def web_set_password(
    request: Request,
    username: str = Form(...),
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    # Validate passwords match
    if new_password != confirm_password:
        return templates.TemplateResponse('auth/set_password.html', {
            'request': request,
            'token': None,
            'error': 'New passwords do not match'
        }, status_code=400)
    
    # Find user by username
    user = (await db.execute(select(User).where(User.username == username))).scalar_one_or_none()
    if not user:
        return templates.TemplateResponse('auth/set_password.html', {
            'request': request,
            'token': None,
            'error': 'Invalid username or password'
        }, status_code=400)
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        return templates.TemplateResponse('auth/set_password.html', {
            'request': request,
            'token': None,
            'error': 'Invalid username or password'
        }, status_code=400)
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    # Auto-login after password change
    request.session['user_id'] = user.id
    
    # Redirect to profile completion if needed
    if not user.profile_completed:
        return RedirectResponse('/web/profile/complete', status_code=303)
    
    return RedirectResponse('/web/projects', status_code=303)


@router.get('/activity')
async def web_activity_feed(
    request: Request,
    activity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_session)
):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user or not user.is_active:
        request.session.clear()
        return RedirectResponse('/web/login', status_code=303)
    
    from datetime import datetime, timedelta
    from app.models.task_extensions import ActivityLog
    
    # Get recent activity logs
    query = select(ActivityLog).where(ActivityLog.workspace_id == user.workspace_id)
    if activity_type:
        query = query.where(ActivityLog.action_type == activity_type)
    query = query.order_by(ActivityLog.created_at.desc()).limit(100)
    
    logs = (await db.execute(query)).scalars().all()
    
    # Enhance activity logs with user names and entity titles
    activities = []
    for log in logs:
        # Get user who performed action
        actor = (await db.execute(select(User).where(User.id == log.user_id))).scalar_one_or_none()
        
        # Get entity title based on type
        entity_title = None
        if log.entity_type == 'task':
            task = (await db.execute(select(Task).where(Task.id == log.entity_id))).scalar_one_or_none()
            entity_title = task.title if task else None
        elif log.entity_type == 'project':
            project = (await db.execute(select(Project).where(Project.id == log.entity_id))).scalar_one_or_none()
            entity_title = project.name if project else None
        
        # Calculate time ago
        time_diff = datetime.utcnow() - log.created_at
        if time_diff.total_seconds() < 60:
            time_ago = "just now"
        elif time_diff.total_seconds() < 3600:
            time_ago = f"{int(time_diff.total_seconds() / 60)}m ago"
        elif time_diff.total_seconds() < 86400:
            time_ago = f"{int(time_diff.total_seconds() / 3600)}h ago"
        else:
            time_ago = f"{int(time_diff.total_seconds() / 86400)}d ago"
        
        activities.append({
            'user_name': actor.full_name or actor.email if actor else 'Unknown',
            'action_type': log.action_type,
            'action_text': log.action_type.replace('_', ' '),
            'entity_type': log.entity_type,
            'entity_id': log.entity_id,
            'entity_title': entity_title,
            'details': log.details,
            'time_ago': time_ago,
            'created_at': log.created_at
        })
    
    # Get workspace stats
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    active_tasks = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == user.workspace_id)
        .where(Task.status != TaskStatus.done)
    )).scalars().all()
    
    completed_week = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == user.workspace_id)
        .where(Task.status == TaskStatus.done)
        .where(Task.updated_at >= datetime.combine(week_ago, datetime.min.time()))
    )).scalars().all()
    
    overdue = (await db.execute(
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.workspace_id == user.workspace_id)
        .where(Task.status != TaskStatus.done)
        .where(Task.due_date < today)
    )).scalars().all()
    
    team_members = (await db.execute(
        select(User)
        .where(User.workspace_id == user.workspace_id)
        .where(User.is_active == True)
    )).scalars().all()
    
    # Calculate per-user statistics
    user_stats = []
    
    if user.is_admin:
        # Admin sees all users' statistics
        for member in team_members:
            # Get tasks assigned to this user
            member_assignments = (await db.execute(
                select(Assignment)
                .where(Assignment.assignee_id == member.id)
            )).scalars().all()
            
            task_ids = [a.task_id for a in member_assignments]
            
            if task_ids:
                # Get all tasks for this user
                member_tasks = (await db.execute(
                    select(Task)
                    .where(Task.id.in_(task_ids))
                )).scalars().all()
                
                # Tasks completed in the last month
                completed_month = [t for t in member_tasks 
                                  if t.status == TaskStatus.done 
                                  and t.updated_at 
                                  and t.updated_at.date() >= month_ago]
                
                # Tasks completed late (had due date, completed after due date)
                completed_late = [t for t in completed_month
                                 if t.due_date and t.updated_at 
                                 and t.updated_at.date() > t.due_date]
                
                # Currently overdue tasks
                overdue_tasks = [t for t in member_tasks
                                if t.status != TaskStatus.done
                                and t.due_date
                                and t.due_date < today]
                
                # Currently active (in progress) tasks
                active_member_tasks = [t for t in member_tasks
                                      if t.status == TaskStatus.in_progress]
                
                # Get current task (most recently updated in-progress task)
                current_task = None
                if active_member_tasks:
                    current_task = sorted(active_member_tasks, 
                                        key=lambda x: x.updated_at if x.updated_at else x.created_at,
                                        reverse=True)[0]
                
                user_stats.append({
                    'user_id': member.id,
                    'user_name': member.full_name or member.email,
                    'user_email': member.email,
                    'completed_month': len(completed_month),
                    'completed_late': len(completed_late),
                    'overdue_count': len(overdue_tasks),
                    'active_count': len(active_member_tasks),
                    'current_task': current_task.title if current_task else None,
                    'current_task_id': current_task.id if current_task else None
                })
    else:
        # Regular user sees only their own statistics
        member_assignments = (await db.execute(
            select(Assignment)
            .where(Assignment.assignee_id == user.id)
        )).scalars().all()
        
        task_ids = [a.task_id for a in member_assignments]
        
        if task_ids:
            member_tasks = (await db.execute(
                select(Task)
                .where(Task.id.in_(task_ids))
            )).scalars().all()
            
            # Tasks completed in the last month
            completed_month = [t for t in member_tasks 
                              if t.status == TaskStatus.done 
                              and t.updated_at 
                              and t.updated_at.date() >= month_ago]
            
            # Separate completed on time vs late
            completed_on_time = []
            completed_late = []
            
            for t in completed_month:
                if t.due_date and t.updated_at:
                    if t.updated_at.date() > t.due_date:
                        completed_late.append(t)
                    else:
                        completed_on_time.append(t)
                else:
                    # No due date set, just mark as completed
                    completed_on_time.append(t)
            
            # Currently overdue tasks
            overdue_tasks = [t for t in member_tasks
                            if t.status != TaskStatus.done
                            and t.due_date
                            and t.due_date < today]
            
            # Currently active tasks
            active_member_tasks = [t for t in member_tasks
                                  if t.status == TaskStatus.in_progress]
            
            user_stats.append({
                'user_id': user.id,
                'user_name': user.full_name or user.email,
                'user_email': user.email,
                'completed_month': len(completed_month),
                'completed_on_time': len(completed_on_time),
                'completed_late': len(completed_late),
                'completed_late_tasks': completed_late,
                'overdue_count': len(overdue_tasks),
                'overdue_tasks': overdue_tasks,
                'active_count': len(active_member_tasks)
            })
    
    stats = {
        'active_tasks': len(active_tasks),
        'completed_week': len(completed_week),
        'overdue': len(overdue),
        'team_members': len(team_members)
    }
    
    return templates.TemplateResponse('activity/feed.html', {
        'request': request,
        'user': user,
        'activities': activities,
        'stats': stats,
        'user_stats': user_stats
    })


# --------------------------
# Workload View (Asana-inspired)
# --------------------------
@router.get('/workload', response_class=HTMLResponse)
async def web_workload(
    request: Request,
    project_id: int = None,
    time_range: str = 'week',
    db: AsyncSession = Depends(get_session)
):
    """Team workload visualization"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse('/web/login', status_code=303)
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        return RedirectResponse('/web/login', status_code=303)
    
    from app.models.task import Task
    from app.models.assignment import Assignment
    from app.models.project import Project
    from app.models.project_member import ProjectMember
    from datetime import timedelta
    
    today = date.today()
    
    # Determine date range
    if time_range == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif time_range == 'month':
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
    else:  # quarter
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = (start_date + timedelta(days=92)).replace(day=1) - timedelta(days=1)
    
    # Get accessible projects
    if user.is_admin:
        projects_query = select(Project).where(
            Project.workspace_id == user.workspace_id,
            Project.is_archived == False
        )
    else:
        projects_query = (
            select(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(
                Project.workspace_id == user.workspace_id,
                ProjectMember.user_id == user_id,
                Project.is_archived == False
            )
        )
    projects = (await db.execute(projects_query)).scalars().all()
    project_ids = [p.id for p in projects]
    
    if project_id and project_id in project_ids:
        project_ids = [project_id]
    
    # Base task query for active tasks
    task_query = select(Task).where(
        Task.project_id.in_(project_ids),
        Task.is_archived == False,
        Task.status != 'done'
    )
    all_tasks = (await db.execute(task_query)).scalars().all()
    
    # Get assignments
    task_ids = [t.id for t in all_tasks]
    assignments = (await db.execute(
        select(Assignment.task_id, Assignment.user_id)
        .where(Assignment.task_id.in_(task_ids))
    )).all() if task_ids else []
    
    assignments_map = {}
    for a in assignments:
        if a.task_id not in assignments_map:
            assignments_map[a.task_id] = []
        assignments_map[a.task_id].append(a.user_id)
    
    # Get team members
    team_members = (await db.execute(
        select(User).where(User.workspace_id == user.workspace_id, User.is_active == True)
    )).scalars().all()
    
    # Calculate workload per member
    team_workload = []
    for member in team_members:
        member_tasks = [t for t in all_tasks if member.id in assignments_map.get(t.id, [])]
        todo_count = len([t for t in member_tasks if t.status.value == 'todo'])
        in_progress_count = len([t for t in member_tasks if t.status.value == 'in_progress'])
        blocked_count = len([t for t in member_tasks if t.status.value == 'blocked'])
        overdue_count = len([t for t in member_tasks if t.due_date and t.due_date < today])
        
        team_workload.append({
            'id': member.id,
            'username': member.username,
            'full_name': member.full_name,
            'task_count': len(member_tasks),
            'todo_count': todo_count,
            'in_progress_count': in_progress_count,
            'blocked_count': blocked_count,
            'overdue_count': overdue_count,
        })
    
    # Sort by task count (busiest first)
    team_workload.sort(key=lambda x: x['task_count'], reverse=True)
    
    # Calculate summary stats
    total_tasks = len(all_tasks)
    in_progress_tasks = len([t for t in all_tasks if t.status.value == 'in_progress'])
    overdue_tasks = len([t for t in all_tasks if t.due_date and t.due_date < today])
    unassigned_tasks = len([t for t in all_tasks if t.id not in assignments_map or not assignments_map[t.id]])
    
    # Priority breakdown
    priority_breakdown = {
        'critical': len([t for t in all_tasks if t.priority.value == 'critical']),
        'high': len([t for t in all_tasks if t.priority.value == 'high']),
        'medium': len([t for t in all_tasks if t.priority.value == 'medium']),
        'low': len([t for t in all_tasks if t.priority.value == 'low']),
    }
    
    # Due date breakdown
    week_end = today + timedelta(days=(6 - today.weekday()))
    due_breakdown = {
        'overdue': len([t for t in all_tasks if t.due_date and t.due_date < today]),
        'today': len([t for t in all_tasks if t.due_date and t.due_date == today]),
        'this_week': len([t for t in all_tasks if t.due_date and today < t.due_date <= week_end]),
        'later': len([t for t in all_tasks if t.due_date and t.due_date > week_end]),
        'no_date': len([t for t in all_tasks if not t.due_date]),
    }
    
    # Unassigned tasks list with project names
    project_names = {p.id: p.name for p in projects}
    unassigned_task_list = []
    for t in all_tasks:
        if t.id not in assignments_map or not assignments_map[t.id]:
            unassigned_task_list.append({
                'id': t.id,
                'title': t.title,
                'priority': t.priority.value,
                'due_date': t.due_date,
                'project_name': project_names.get(t.project_id, 'Unknown')
            })
    
    return templates.TemplateResponse('workload/index.html', {
        'request': request,
        'user': user,
        'projects': projects,
        'selected_project_id': project_id,
        'time_range': time_range,
        'team_workload': team_workload,
        'total_tasks': total_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'unassigned_tasks': unassigned_tasks,
        'priority_breakdown': priority_breakdown,
        'due_breakdown': due_breakdown,
        'unassigned_task_list': unassigned_task_list,
    })


# Goals feature removed - routes deleted


# ============ TASK TEMPLATES ============

@router.get('/templates', response_class=HTMLResponse)
async def templates_page(
    request: Request,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Task templates management page"""
    from app.models.task_extensions import TaskTemplate
    if not user or not user.workspace_id:
        return RedirectResponse(url='/web/login', status_code=303)
    
    # Get templates for this workspace
    templates_list = (await db.execute(
        select(TaskTemplate).where(
            TaskTemplate.workspace_id == user.workspace_id,
            or_(TaskTemplate.is_shared == True, TaskTemplate.created_by_id == user.id)
        ).order_by(TaskTemplate.use_count.desc())
    )).scalars().all()
    
    # Get projects for the "use template" modal
    projects = (await db.execute(
        select(Project).where(Project.workspace_id == user.workspace_id, Project.is_archived == False)
        .order_by(Project.name)
    )).scalars().all()
    
    # Get workspace members
    members = (await db.execute(
        select(User).where(User.workspace_id == user.workspace_id, User.is_active == True)
        .order_by(User.full_name)
    )).scalars().all()
    
    return templates.TemplateResponse("templates/index.html", {
        "request": request,
        "user": user,
        "templates": templates_list,
        "projects": projects,
        "members": members
    })


@router.post('/templates/create')
async def create_template(
    request: Request,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Create a new task template"""
    from app.models.task_extensions import TaskTemplate
    if not user or not user.workspace_id:
        return RedirectResponse(url='/web/login', status_code=303)
    
    form = await request.form()
    
    template = TaskTemplate(
        workspace_id=user.workspace_id,
        name=form.get('name'),
        title_template=form.get('title_template'),
        description_template=form.get('description_template') or None,
        priority=form.get('priority', 'medium'),
        estimated_hours=float(form.get('estimated_hours')) if form.get('estimated_hours') else None,
        default_tags=form.get('default_tags') or None,
        is_shared='is_shared' in form,
        created_by_id=user.id
    )
    
    db.add(template)
    await db.commit()
    
    return RedirectResponse(url='/web/templates', status_code=303)


@router.post('/templates/{template_id}/update')
async def update_template(
    request: Request,
    template_id: int,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Update a task template"""
    from app.models.task_extensions import TaskTemplate
    if not user or not user.workspace_id:
        return RedirectResponse(url='/web/login', status_code=303)
    
    template = (await db.execute(
        select(TaskTemplate).where(
            TaskTemplate.id == template_id,
            TaskTemplate.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not template:
        return RedirectResponse(url='/web/templates', status_code=303)
    
    form = await request.form()
    
    template.name = form.get('name')
    template.title_template = form.get('title_template')
    template.description_template = form.get('description_template') or None
    template.priority = form.get('priority', 'medium')
    template.estimated_hours = float(form.get('estimated_hours')) if form.get('estimated_hours') else None
    template.default_tags = form.get('default_tags') or None
    template.is_shared = 'is_shared' in form
    
    await db.commit()
    
    return RedirectResponse(url='/web/templates', status_code=303)


@router.post('/templates/{template_id}/delete')
async def delete_template(
    template_id: int,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Delete a task template"""
    from app.models.task_extensions import TaskTemplate
    if not user or not user.workspace_id:
        return JSONResponse(status_code=401, content={'error': 'Unauthorized'})
    
    template = (await db.execute(
        select(TaskTemplate).where(
            TaskTemplate.id == template_id,
            TaskTemplate.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not template:
        return JSONResponse(status_code=404, content={'error': 'Template not found'})
    
    await db.delete(template)
    await db.commit()
    
    return JSONResponse(status_code=200, content={'success': True})


@router.post('/templates/use')
async def use_template(
    request: Request,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """Create a task from a template"""
    from app.models.task_extensions import TaskTemplate
    if not user or not user.workspace_id:
        return RedirectResponse(url='/web/login', status_code=303)
    
    form = await request.form()
    template_id = int(form.get('template_id'))
    
    template = (await db.execute(
        select(TaskTemplate).where(
            TaskTemplate.id == template_id,
            TaskTemplate.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    
    if not template:
        return RedirectResponse(url='/web/templates', status_code=303)
    
    # Create the task from template
    from datetime import datetime
    task = Task(
        title=form.get('title') or template.title_template,
        description=template.description_template,
        project_id=int(form.get('project_id')),
        priority=template.priority,
        status='pending',
        creator_id=user.id,
        due_date=datetime.strptime(form.get('due_date'), '%Y-%m-%d') if form.get('due_date') else None
    )
    
    db.add(task)
    await db.flush()
    
    # Auto-assign to creator
    from app.models.assignment import Assignment
    assignment = Assignment(task_id=task.id, assignee_id=user.id)
    db.add(assignment)
    
    # If specific user was assigned, add them too
    assigned_to_id = form.get('assigned_to_id')
    if assigned_to_id and int(assigned_to_id) != user.id:
        extra_assignment = Assignment(task_id=task.id, assignee_id=int(assigned_to_id))
        db.add(extra_assignment)
    
    # Increment template use count
    template.use_count += 1
    
    await db.commit()
    await db.refresh(task)
    
    return RedirectResponse(url=f'/web/tasks/{task.id}', status_code=303)


# Calls feature removed - routes deleted


# =====================================================
# IT KNOWLEDGE BASE - Solutions, Diagnostics, Resolved Cases
# =====================================================

from app.models.knowledge_base import KBDiagnosticTree, KBResolvedCase


@router.get('/knowledge-base', response_class=HTMLResponse)
async def web_knowledge_base(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_session)
):
    """Main Knowledge Base / Solutions page"""
    user = await get_current_user(request, db)

    # Recent articles from SupportArticle
    article_query = select(SupportArticle).where(
        SupportArticle.workspace_id == user.workspace_id,
        SupportArticle.is_active == True
    )
    if category:
        article_query = article_query.where(SupportArticle.category == category)
    article_query = article_query.order_by(SupportArticle.created_at.desc()).limit(12)
    recent_articles = (await db.execute(article_query)).scalars().all()

    # Recent resolved cases
    case_query = select(KBResolvedCase).where(
        KBResolvedCase.workspace_id == user.workspace_id
    )
    if category:
        case_query = case_query.where(KBResolvedCase.category == category)
    case_query = case_query.order_by(KBResolvedCase.created_at.desc()).limit(12)
    recent_cases = (await db.execute(case_query)).scalars().all()

    # Categories
    categories = (await db.execute(
        select(SupportCategory).where(
            SupportCategory.workspace_id == user.workspace_id,
            SupportCategory.is_active == True
        ).order_by(SupportCategory.name)
    )).scalars().all()

    return templates.TemplateResponse('knowledge_base/index.html', {
        'request': request,
        'user': user,
        'recent_articles': recent_articles,
        'recent_cases': recent_cases,
        'categories': categories,
        'all_categories': categories,
        'search_query': search or '',
        'active_tab': 'search',
    })


@router.get('/knowledge-base/search', response_class=JSONResponse)
async def web_kb_search(
    request: Request,
    q: str = '',
    db: AsyncSession = Depends(get_session)
):
    """Fuzzy search across articles and resolved cases"""
    user = await get_current_user(request, db)
    if not q.strip():
        return {'results': []}

    search_term = q.strip()
    keywords = [w for w in search_term.lower().split() if len(w) >= 2]
    results = []

    # Search SupportArticle
    for kw in keywords:
        pattern = f'%{kw}%'
        articles = (await db.execute(
            select(SupportArticle).where(
                SupportArticle.workspace_id == user.workspace_id,
                SupportArticle.is_active == True,
                or_(
                    SupportArticle.problem_title.ilike(pattern),
                    SupportArticle.problem_description.ilike(pattern),
                    SupportArticle.problem_keywords.ilike(pattern),
                    SupportArticle.solution_steps.ilike(pattern),
                )
            ).order_by(SupportArticle.times_helpful.desc()).limit(10)
        )).scalars().all()
        for a in articles:
            if not any(r['id'] == f'article-{a.id}' for r in results):
                results.append({
                    'id': f'article-{a.id}',
                    'type': 'article',
                    'title': a.problem_title,
                    'description': a.problem_description[:200],
                    'category': a.category,
                    'tags': a.problem_keywords or '',
                    'is_verified': a.is_verified,
                    'helpful_votes': a.times_helpful,
                    'url': f'/web/knowledge-base/article/{a.id}'
                })

    # Search KBResolvedCase
    for kw in keywords:
        pattern = f'%{kw}%'
        cases = (await db.execute(
            select(KBResolvedCase).where(
                KBResolvedCase.workspace_id == user.workspace_id,
                or_(
                    KBResolvedCase.problem_title.ilike(pattern),
                    KBResolvedCase.problem_description.ilike(pattern),
                    KBResolvedCase.solution_steps.ilike(pattern),
                    KBResolvedCase.error_message.ilike(pattern),
                    KBResolvedCase.tags.ilike(pattern),
                    KBResolvedCase.device_brand.ilike(pattern),
                    KBResolvedCase.root_cause.ilike(pattern),
                )
            ).order_by(KBResolvedCase.helpful_votes.desc()).limit(10)
        )).scalars().all()
        for c in cases:
            if not any(r['id'] == f'case-{c.id}' for r in results):
                results.append({
                    'id': f'case-{c.id}',
                    'type': 'resolved_case',
                    'title': c.problem_title,
                    'description': c.problem_description[:200],
                    'category': c.category,
                    'tags': c.tags or '',
                    'is_verified': c.is_verified,
                    'helpful_votes': c.helpful_votes,
                    'url': f'/web/knowledge-base/resolved/{c.id}'
                })

    return {'results': results[:20]}


@router.get('/knowledge-base/article/{article_id}', response_class=HTMLResponse)
async def web_kb_article_detail(
    request: Request,
    article_id: int,
    db: AsyncSession = Depends(get_session)
):
    """View a single KB article"""
    user = await get_current_user(request, db)
    article = (await db.execute(
        select(SupportArticle).where(
            SupportArticle.id == article_id,
            SupportArticle.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Increment view count
    article.times_shown += 1
    await db.commit()

    # Related articles (same category)
    related_articles = (await db.execute(
        select(SupportArticle).where(
            SupportArticle.workspace_id == user.workspace_id,
            SupportArticle.category == article.category,
            SupportArticle.id != article.id,
            SupportArticle.is_active == True
        ).order_by(SupportArticle.times_helpful.desc()).limit(5)
    )).scalars().all()

    return templates.TemplateResponse('knowledge_base/article.html', {
        'request': request,
        'user': user,
        'article': article,
        'related_articles': related_articles,
    })


@router.post('/knowledge-base/article/{article_id}/rate')
async def web_kb_article_rate(
    request: Request,
    article_id: int,
    helpful: str = Form('true'),
    db: AsyncSession = Depends(get_session)
):
    """Rate an article helpful/not helpful"""
    user = await get_current_user(request, db)
    article = (await db.execute(
        select(SupportArticle).where(
            SupportArticle.id == article_id,
            SupportArticle.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    if article:
        if helpful == 'true':
            article.times_helpful += 1
        else:
            article.times_not_helpful += 1
        # Recalculate success rate
        total = article.times_helpful + article.times_not_helpful
        article.success_rate = (article.times_helpful / total * 100) if total > 0 else 0
        await db.commit()
    return RedirectResponse(url=f'/web/knowledge-base/article/{article_id}', status_code=303)


@router.post('/knowledge-base/articles', response_class=JSONResponse)
async def web_kb_create_article(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Create a new KB article (from the Add Solution modal)"""
    user = await get_current_user(request, db)
    data = await request.json()

    problem_title = (data.get('problem_title') or '').strip()
    problem_description = (data.get('problem_description') or '').strip()
    category = (data.get('category') or '').strip()
    solution_steps = (data.get('solution_steps') or '').strip()

    if not problem_title or not problem_description or not category or not solution_steps:
        return JSONResponse({'error': 'Missing required fields'}, status_code=400)

    article = SupportArticle(
        workspace_id=user.workspace_id,
        problem_title=problem_title,
        problem_description=problem_description,
        problem_keywords=(data.get('keywords') or '').strip(),
        category=category,
        solution_steps=solution_steps,
        solution_source='manual',
        created_by_id=user.id,
        is_active=True,
    )
    db.add(article)
    await db.commit()
    return {'ok': True, 'id': article.id}


# --- Diagnostic Engine routes ---

@router.get('/knowledge-base/diagnostic/start', response_class=JSONResponse)
async def web_kb_diagnostic_start(
    request: Request,
    category: str = '',
    db: AsyncSession = Depends(get_session)
):
    """Get root diagnostic node(s) for a category"""
    user = await get_current_user(request, db)

    # Find root nodes (parent_id is None) for this category
    roots = (await db.execute(
        select(KBDiagnosticTree).where(
            KBDiagnosticTree.workspace_id == user.workspace_id,
            KBDiagnosticTree.parent_id == None,
            KBDiagnosticTree.is_active == True,
            KBDiagnosticTree.category == category
        ).order_by(KBDiagnosticTree.sort_order)
    )).scalars().all()

    if not roots:
        return {'node': None, 'children': []}

    # If single root, return it with its children
    root = roots[0]
    children = (await db.execute(
        select(KBDiagnosticTree).where(
            KBDiagnosticTree.parent_id == root.id,
            KBDiagnosticTree.is_active == True
        ).order_by(KBDiagnosticTree.sort_order)
    )).scalars().all()

    return {
        'node': {
            'id': root.id,
            'title': root.title,
            'node_type': root.node_type,
            'question_text': root.question_text,
            'solution_text': root.solution_text,
        },
        'children': [
            {
                'id': c.id,
                'title': c.title,
                'node_type': c.node_type,
                'question_text': c.question_text,
                'solution_text': c.solution_text,
            } for c in children
        ]
    }


@router.get('/knowledge-base/diagnostic/step/{node_id}', response_class=JSONResponse)
async def web_kb_diagnostic_step(
    request: Request,
    node_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Get a diagnostic tree node and its children"""
    user = await get_current_user(request, db)

    node = (await db.execute(
        select(KBDiagnosticTree).where(
            KBDiagnosticTree.id == node_id,
            KBDiagnosticTree.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()

    if not node:
        return {'node': None, 'children': []}

    children = (await db.execute(
        select(KBDiagnosticTree).where(
            KBDiagnosticTree.parent_id == node.id,
            KBDiagnosticTree.is_active == True
        ).order_by(KBDiagnosticTree.sort_order)
    )).scalars().all()

    return {
        'node': {
            'id': node.id,
            'title': node.title,
            'node_type': node.node_type,
            'question_text': node.question_text,
            'solution_text': node.solution_text,
        },
        'children': [
            {
                'id': c.id,
                'title': c.title,
                'node_type': c.node_type,
                'question_text': c.question_text,
                'solution_text': c.solution_text,
            } for c in children
        ]
    }


@router.post('/knowledge-base/diagnostic/rate', response_class=JSONResponse)
async def web_kb_diagnostic_rate(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Rate a diagnostic solution node"""
    user = await get_current_user(request, db)
    data = await request.json()
    # Placeholder acknowledgment - could track per-node feedback in the future
    return {'ok': True}


# --- Resolved Cases routes ---

@router.get('/knowledge-base/resolved-cases', response_class=HTMLResponse)
async def web_kb_resolved_cases(
    request: Request,
    search: Optional[str] = None,
    category: Optional[str] = None,
    device_type: Optional[str] = None,
    verified: Optional[str] = None,
    db: AsyncSession = Depends(get_session)
):
    """List resolved cases"""
    user = await get_current_user(request, db)

    query = select(KBResolvedCase).where(
        KBResolvedCase.workspace_id == user.workspace_id
    )

    if search:
        pattern = f'%{search.strip()}%'
        query = query.where(or_(
            KBResolvedCase.problem_title.ilike(pattern),
            KBResolvedCase.problem_description.ilike(pattern),
            KBResolvedCase.solution_steps.ilike(pattern),
            KBResolvedCase.error_message.ilike(pattern),
            KBResolvedCase.tags.ilike(pattern),
            KBResolvedCase.device_brand.ilike(pattern),
            KBResolvedCase.ticket_number.ilike(pattern),
        ))
    if category:
        query = query.where(KBResolvedCase.category == category)
    if device_type:
        query = query.where(KBResolvedCase.device_type == device_type)
    if verified == 'yes':
        query = query.where(KBResolvedCase.is_verified == True)

    query = query.order_by(KBResolvedCase.created_at.desc()).limit(50)
    cases = (await db.execute(query)).scalars().all()

    return templates.TemplateResponse('knowledge_base/resolved_cases.html', {
        'request': request,
        'user': user,
        'cases': cases,
        'search_query': search or '',
        'category_filter': category or '',
        'device_filter': device_type or '',
        'verified_filter': verified or '',
    })


@router.get('/knowledge-base/resolved-cases/new', response_class=HTMLResponse)
async def web_kb_resolved_case_new(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """Form to log a new resolved case"""
    user = await get_current_user(request, db)
    return templates.TemplateResponse('knowledge_base/resolved_new.html', {
        'request': request,
        'user': user,
        'error': None,
        'form_data': None,
    })


@router.post('/knowledge-base/resolved-cases/new')
async def web_kb_resolved_case_create(
    request: Request,
    problem_title: str = Form(...),
    problem_description: str = Form(...),
    category: str = Form(...),
    solution_steps: str = Form(...),
    error_message: str = Form(''),
    device_type: str = Form(''),
    device_brand: str = Form(''),
    device_model: str = Form(''),
    connection_type: str = Form(''),
    tags: str = Form(''),
    root_cause: str = Form(''),
    time_to_resolve: Optional[int] = Form(None),
    ticket_number: str = Form(''),
    db: AsyncSession = Depends(get_session)
):
    """Save a new resolved case"""
    user = await get_current_user(request, db)

    if not problem_title.strip() or not problem_description.strip() or not solution_steps.strip():
        return templates.TemplateResponse('knowledge_base/resolved_new.html', {
            'request': request,
            'user': user,
            'error': 'Problem title, description, and solution steps are required.',
            'form_data': {
                'problem_title': problem_title,
                'problem_description': problem_description,
                'category': category,
                'solution_steps': solution_steps,
                'error_message': error_message,
                'device_type': device_type,
                'device_brand': device_brand,
                'device_model': device_model,
                'connection_type': connection_type,
                'tags': tags,
                'root_cause': root_cause,
                'time_to_resolve': time_to_resolve,
                'ticket_number': ticket_number,
            }
        }, status_code=400)

    case = KBResolvedCase(
        workspace_id=user.workspace_id,
        problem_title=problem_title.strip(),
        problem_description=problem_description.strip(),
        error_message=error_message.strip() or None,
        category=category.strip(),
        device_type=device_type.strip() or None,
        device_brand=device_brand.strip() or None,
        device_model=device_model.strip() or None,
        connection_type=connection_type.strip() or None,
        tags=tags.strip() or None,
        solution_steps=solution_steps.strip(),
        root_cause=root_cause.strip() or None,
        time_to_resolve=time_to_resolve,
        ticket_number=ticket_number.strip() or None,
        resolved_by_id=user.id,
        resolved_by_name=user.full_name or user.username,
    )
    db.add(case)
    await db.commit()

    request.session['success_message'] = 'Resolved case logged successfully! Thank you for contributing to the knowledge base.'
    return RedirectResponse(url='/web/knowledge-base/resolved-cases', status_code=303)


@router.get('/knowledge-base/resolved/{case_id}', response_class=HTMLResponse)
async def web_kb_resolved_detail(
    request: Request,
    case_id: int,
    db: AsyncSession = Depends(get_session)
):
    """View a resolved case in detail"""
    user = await get_current_user(request, db)
    case = (await db.execute(
        select(KBResolvedCase).where(
            KBResolvedCase.id == case_id,
            KBResolvedCase.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Resolved case not found")

    # Increment view count
    case.times_viewed += 1
    await db.commit()

    # Related cases (same category)
    related_cases = (await db.execute(
        select(KBResolvedCase).where(
            KBResolvedCase.workspace_id == user.workspace_id,
            KBResolvedCase.category == case.category,
            KBResolvedCase.id != case.id
        ).order_by(KBResolvedCase.helpful_votes.desc()).limit(5)
    )).scalars().all()

    return templates.TemplateResponse('knowledge_base/resolved_detail.html', {
        'request': request,
        'user': user,
        'case': case,
        'related_cases': related_cases,
    })


@router.post('/knowledge-base/resolved/{case_id}/rate')
async def web_kb_resolved_rate(
    request: Request,
    case_id: int,
    helpful: str = Form('true'),
    db: AsyncSession = Depends(get_session)
):
    """Rate a resolved case"""
    user = await get_current_user(request, db)
    case = (await db.execute(
        select(KBResolvedCase).where(
            KBResolvedCase.id == case_id,
            KBResolvedCase.workspace_id == user.workspace_id
        )
    )).scalar_one_or_none()
    if case:
        if helpful == 'true':
            case.helpful_votes += 1
        else:
            case.not_helpful_votes += 1
        await db.commit()
    return RedirectResponse(url=f'/web/knowledge-base/resolved/{case_id}', status_code=303)
