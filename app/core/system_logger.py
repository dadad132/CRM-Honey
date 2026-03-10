"""
System diagnostic logger - writes structured logs to the SystemLog table.
Logs are auto-cleaned after 7 days to keep DB size small.
"""

import asyncio
import traceback
from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.models.system_log import SystemLog


async def write_log(
    level: str,
    category: str,
    source: str,
    message: str,
    details: Optional[str] = None,
    workspace_id: Optional[int] = None,
):
    """Write a log entry to the SystemLog table. Fire-and-forget safe."""
    try:
        async with AsyncSession(engine) as db:
            # Truncate details to 500 chars to keep DB small
            if details and len(details) > 500:
                details = details[:497] + "..."
            entry = SystemLog(
                timestamp=datetime.utcnow(),
                level=level,
                category=category,
                source=source,
                message=message[:200],  # Cap message length
                details=details,
                workspace_id=workspace_id,
            )
            db.add(entry)
            await db.commit()
    except Exception:
        # Never let logging crash the caller
        pass


def log_fire_and_forget(
    level: str,
    category: str,
    source: str,
    message: str,
    details: Optional[str] = None,
    workspace_id: Optional[int] = None,
):
    """Schedule a log write without awaiting it. Safe to call from sync or async code."""
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(write_log(level, category, source, message, details, workspace_id))
    except RuntimeError:
        # No running loop — skip
        pass


async def cleanup_old_logs():
    """Delete SystemLog entries older than 7 days."""
    try:
        async with AsyncSession(engine) as db:
            cutoff = datetime.utcnow() - timedelta(days=7)
            from sqlalchemy import delete as sa_delete
            stmt = sa_delete(SystemLog).where(SystemLog.timestamp < cutoff)
            result = await db.execute(stmt)
            await db.commit()
            deleted = result.rowcount  # type: ignore
            if deleted:
                print(f"[SystemLog] Cleaned up {deleted} log entries older than 7 days")
    except Exception as e:
        print(f"[SystemLog] Error during cleanup: {e}")


async def start_log_cleanup_scheduler():
    """Background task that cleans up old logs every 6 hours."""
    print("[SystemLog] Log cleanup scheduler started (runs every 6 hours, deletes logs older than 7 days)")
    while True:
        try:
            await asyncio.sleep(6 * 3600)  # Every 6 hours
            await cleanup_old_logs()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[SystemLog] Cleanup scheduler error: {e}")
            await asyncio.sleep(3600)  # Retry in 1 hour on error
