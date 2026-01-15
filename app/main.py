from fastapi import FastAPI, Request, Depends, HTTPException
# restart trigger: updated timestamp
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import os

from app.core.config import get_settings
from app.core.database import lifespan, get_session
from app.api.routes import auth as auth_routes
from app.api.routes import users as users_routes
from app.api.routes import projects as projects_routes
from app.api.routes import tasks as tasks_routes
from app.models.user import User

settings = get_settings()

# Disable default API docs - we'll add custom protected ones
app = FastAPI(
    title=settings.app_name, 
    debug=settings.debug, 
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# GZip compression for faster page loads (compresses responses > 500 bytes)
app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Workspace injection middleware - adds workspace to all requests
# MUST be added BEFORE SessionMiddleware so it runs AFTER (middleware order is reversed)
from starlette.middleware.base import BaseHTTPMiddleware
from functools import lru_cache
import time

# Simple in-memory cache for workspace data (reduces DB queries)
_workspace_cache = {}  # {workspace_id: (workspace_data, timestamp)}
_user_workspace_cache = {}  # {user_id: (workspace_id, timestamp)}
CACHE_TTL = 300  # Cache for 5 minutes

class WorkspaceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip workspace lookup for static files and health checks
        path = request.url.path
        if path.startswith('/uploads') or path == '/health' or path.startswith('/api/'):
            return await call_next(request)
        
        user_id = None
        
        # Safely check for session
        try:
            if "session" in request.scope:
                user_id = request.scope["session"].get('user_id')
        except Exception:
            pass
        
        if user_id:
            try:
                current_time = time.time()
                workspace = None
                
                # Check user->workspace cache first
                if user_id in _user_workspace_cache:
                    workspace_id, cached_time = _user_workspace_cache[user_id]
                    if current_time - cached_time < CACHE_TTL:
                        # Check workspace cache
                        if workspace_id in _workspace_cache:
                            ws_data, ws_time = _workspace_cache[workspace_id]
                            if current_time - ws_time < CACHE_TTL:
                                request.state.workspace = ws_data
                                return await call_next(request)
                
                # Cache miss - fetch from database
                from app.core.database import get_session
                from app.models.workspace import Workspace
                async for db in get_session():
                    user = (await db.execute(
                        select(User).where(User.id == user_id)
                    )).scalar_one_or_none()
                    
                    if user and user.workspace_id:
                        workspace = (await db.execute(
                            select(Workspace).where(Workspace.id == user.workspace_id)
                        )).scalar_one_or_none()
                        
                        if workspace:
                            # Update caches
                            _user_workspace_cache[user_id] = (user.workspace_id, current_time)
                            _workspace_cache[user.workspace_id] = (workspace, current_time)
                            request.state.workspace = workspace
                    break
            except Exception:
                pass
        
        response = await call_next(request)
        return response

app.add_middleware(WorkspaceMiddleware)

# Cache control middleware for static assets
class CacheControlMiddleware(BaseHTTPMiddleware):
    """Add cache headers to static files for better performance"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Cache uploaded files (images, attachments) for 1 day
        if request.url.path.startswith('/uploads'):
            response.headers['Cache-Control'] = 'public, max-age=86400'
        return response

app.add_middleware(CacheControlMiddleware)

# Session middleware for server-rendered web UI
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Import templates from web routes to get the enhanced version with workspace injection
from app.web.routes import templates

# Mount uploads directory for serving uploaded files (logos, attachments, etc.)
BASE_DIR = Path(__file__).resolve().parent
uploads_path = os.path.join(BASE_DIR, "uploads")
os.makedirs(uploads_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")


@app.get("/health")
async def health():
    return {"status": "ok"}


# API documentation routes - DISABLED for all users
# Documentation is completely hidden from all users including admins
# Uncomment routes below if you need to enable API docs temporarily

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html(request: Request):
#     """Swagger UI - Disabled"""
#     raise HTTPException(status_code=404, detail="Not found")


# @app.get("/redoc", include_in_schema=False)
# async def redoc_html(request: Request):
#     """ReDoc - Disabled"""
#     raise HTTPException(status_code=404, detail="Not found")


# @app.get("/openapi.json", include_in_schema=False)
# async def get_open_api_endpoint(request: Request):
#     """OpenAPI JSON - Disabled"""
#     raise HTTPException(status_code=404, detail="Not found")


# API routers
app.include_router(auth_routes.router, prefix="/api")
app.include_router(users_routes.router, prefix="/api")
app.include_router(projects_routes.router, prefix="/api")
app.include_router(tasks_routes.router, prefix="/api")
from app.api.routes import system as system_routes
app.include_router(system_routes.router, prefix="/api")
from app.web import routes as web_routes  # noqa: E402
app.include_router(web_routes.router, prefix="/web")


# Minimal server-rendered pages
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Get workspace from request state (added by middleware)
    workspace = getattr(request.state, 'workspace', None)
    # Render the landing page template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "workspace": workspace
    })
