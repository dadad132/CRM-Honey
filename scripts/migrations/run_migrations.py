#!/usr/bin/env python3
"""
Run all pending database migrations.
Usage: python scripts/migrations/run_migrations.py
"""
import sqlite3
import os

# Find the database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data.db')

def run_migrations():
    print(f"Running migrations on: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get existing columns for each table
    def get_columns(table):
        cursor.execute(f"PRAGMA table_info({table})")
        return [row[1] for row in cursor.fetchall()]
    
    migrations = []
    
    # Migration 002: Bubbles chat and What Changed feature
    # SupportConversation columns
    if 'supportconversation' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        cols = get_columns('supportconversation')
        if 'was_helpful' not in cols:
            cursor.execute("ALTER TABLE supportconversation ADD COLUMN was_helpful BOOLEAN DEFAULT 0")
            migrations.append("Added: supportconversation.was_helpful")
        if 'resolution_type' not in cols:
            cursor.execute("ALTER TABLE supportconversation ADD COLUMN resolution_type VARCHAR")
            migrations.append("Added: supportconversation.resolution_type")
    
    # User columns for "What Changed" feature
    if 'user' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
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
    
    conn.commit()
    conn.close()
    
    if migrations:
        print("Migrations applied:")
        for m in migrations:
            print(f"  ✓ {m}")
    else:
        print("No new migrations needed - database is up to date.")
    
    print("Done!")

if __name__ == "__main__":
    run_migrations()
