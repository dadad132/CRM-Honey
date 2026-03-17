"""
Data Retention & Database Maintenance
Automatically cleans up old data to keep the database small and fast.
Runs alongside the system log cleanup scheduler.

Retention policies:
- Notifications (read/dismissed): 90 days
- Support bot conversations: 90 days
- User behavior tracking: 90 days
- Processed email records: 30 days
- SQLite VACUUM: runs after cleanup to reclaim disk space
"""

import asyncio
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import delete as sa_delete

from app.core.database import engine


async def cleanup_old_data():
    """Run all data retention cleanup tasks."""
    total_deleted = 0

    try:
        async with AsyncSession(engine) as db:
            now = datetime.utcnow()

            # 1. Notifications — delete read/dismissed older than 90 days
            try:
                from app.models.notification import Notification
                cutoff_90 = now - timedelta(days=90)
                stmt = sa_delete(Notification).where(
                    Notification.created_at < cutoff_90,
                    Notification.read_at.isnot(None)
                )
                result = await db.execute(stmt)
                count = result.rowcount or 0
                if count:
                    print(f"[DataRetention] Cleaned {count} old read notifications (>90 days)")
                total_deleted += count
            except Exception as e:
                print(f"[DataRetention] Notification cleanup error: {e}")

            # 2. Support bot conversations — delete older than 90 days
            try:
                from app.models.support_kb import SupportConversation
                stmt = sa_delete(SupportConversation).where(
                    SupportConversation.created_at < cutoff_90
                )
                result = await db.execute(stmt)
                count = result.rowcount or 0
                if count:
                    print(f"[DataRetention] Cleaned {count} old support conversations (>90 days)")
                total_deleted += count
            except Exception as e:
                if "no such table" not in str(e).lower():
                    print(f"[DataRetention] SupportConversation cleanup error: {e}")

            # 3. User behavior tracking — delete older than 90 days
            try:
                from app.models.user_behavior import UserBehavior
                stmt = sa_delete(UserBehavior).where(
                    UserBehavior.created_at < cutoff_90
                )
                result = await db.execute(stmt)
                count = result.rowcount or 0
                if count:
                    print(f"[DataRetention] Cleaned {count} old user behavior records (>90 days)")
                total_deleted += count
            except Exception as e:
                if "no such table" not in str(e).lower():
                    print(f"[DataRetention] UserBehavior cleanup error: {e}")

            # 4. Processed email records — delete older than 30 days
            # Only needs 7 days for dedup but keeping 30 for safety margin
            try:
                from app.models.processed_mail import ProcessedMail
                cutoff_30 = now - timedelta(days=30)
                stmt = sa_delete(ProcessedMail).where(
                    ProcessedMail.processed_at < cutoff_30
                )
                result = await db.execute(stmt)
                count = result.rowcount or 0
                if count:
                    print(f"[DataRetention] Cleaned {count} old processed email records (>30 days)")
                total_deleted += count
            except Exception as e:
                if "no such table" not in str(e).lower():
                    print(f"[DataRetention] ProcessedMail cleanup error: {e}")

            await db.commit()

    except Exception as e:
        print(f"[DataRetention] Error during data cleanup: {e}")

    # 5. SQLite VACUUM — reclaim disk space after deletions
    if total_deleted > 0:
        try:
            db_path = Path("data.db")
            if db_path.exists():
                size_before = db_path.stat().st_size
                # VACUUM must run outside of SQLAlchemy (requires exclusive lock, no transaction)
                await asyncio.to_thread(_vacuum_database, str(db_path))
                size_after = db_path.stat().st_size
                saved_kb = (size_before - size_after) / 1024
                if saved_kb > 1:
                    print(f"[DataRetention] VACUUM reclaimed {saved_kb:.1f} KB")
        except Exception as e:
            print(f"[DataRetention] VACUUM error (non-critical): {e}")

    if total_deleted:
        print(f"[DataRetention] Total cleaned: {total_deleted} records")


def _vacuum_database(db_path: str):
    """Run SQLite VACUUM in a thread (blocking operation)."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("VACUUM")
    finally:
        conn.close()


async def start_data_retention_scheduler():
    """Background task that runs data retention cleanup every 12 hours."""
    print("[DataRetention] Data retention scheduler started (runs every 12 hours)")
    while True:
        try:
            await asyncio.sleep(12 * 3600)  # Every 12 hours
            await cleanup_old_data()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[DataRetention] Scheduler error: {e}")
            await asyncio.sleep(3600)  # Retry in 1 hour on error
