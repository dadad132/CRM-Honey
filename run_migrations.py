#!/usr/bin/env python3
"""
Run all pending database migrations.
Usage: python run_migrations.py
"""
import sqlite3
import os

# Find the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def run_migrations():
    print(f"Running migrations on: {DB_PATH}")
    
    if not os.path.exists(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get existing columns for each table
    def get_columns(table):
        cursor.execute(f"PRAGMA table_info({table})")
        return [row[1] for row in cursor.fetchall()]
    
    # Get list of tables
    tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    
    migrations = []
    
    # Migration: SupportConversation columns
    if 'supportconversation' in tables:
        cols = get_columns('supportconversation')
        if 'was_helpful' not in cols:
            cursor.execute("ALTER TABLE supportconversation ADD COLUMN was_helpful BOOLEAN DEFAULT 0")
            migrations.append("Added: supportconversation.was_helpful")
        if 'resolution_type' not in cols:
            cursor.execute("ALTER TABLE supportconversation ADD COLUMN resolution_type VARCHAR")
            migrations.append("Added: supportconversation.resolution_type")
    
    # Migration: User columns
    if 'user' in tables:
        cols = get_columns('user')
        if 'last_seen_at' not in cols:
            cursor.execute("ALTER TABLE user ADD COLUMN last_seen_at DATETIME")
            migrations.append("Added: user.last_seen_at")
        if 'away_summary_preference' not in cols:
            cursor.execute("ALTER TABLE user ADD COLUMN away_summary_preference VARCHAR DEFAULT 'ask'")
            migrations.append("Added: user.away_summary_preference")
        if 'show_bubbles_analytics' not in cols:
            cursor.execute("ALTER TABLE user ADD COLUMN show_bubbles_analytics BOOLEAN DEFAULT 0")
            migrations.append("Added: user.show_bubbles_analytics")
    
    # Migration: Bubbles feedback table
    if 'bubbles_feedback' not in tables:
        cursor.execute("""
            CREATE TABLE bubbles_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id VARCHAR(100),
                message TEXT,
                response TEXT,
                rating VARCHAR(20),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        migrations.append("Created: bubbles_feedback table")
    
    # Migration: Bubbles analytics table
    if 'bubbles_analytics' not in tables:
        cursor.execute("""
            CREATE TABLE bubbles_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id VARCHAR(100),
                event_type VARCHAR(50),
                event_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        migrations.append("Created: bubbles_analytics table")
    
    conn.commit()
    conn.close()
    
    if migrations:
        print("\n✅ Migrations applied:")
        for m in migrations:
            print(f"  ✓ {m}")
    else:
        print("\n✅ No new migrations needed - database is up to date.")
    
    print("\nDone!")

if __name__ == "__main__":
    run_migrations()
