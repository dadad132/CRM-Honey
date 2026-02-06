#!/usr/bin/env python3
"""
Support Knowledge Base Migration Script
========================================
Creates all necessary tables and indexes for the AI Support Assistant chatbot.

Features:
- SupportCategory: Organize solutions by category
- SupportArticle: Knowledge base of problems and solutions
- SupportConversation: Track user conversations with the assistant

Usage:
    python create_support_kb_tables.py

This script is idempotent - safe to run multiple times.
"""
import sqlite3
import os
import subprocess
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = ['httpx']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"[*] Installing required packages: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print(f"✓ Installed {', '.join(missing_packages)}")

def create_tables():
    """Create support knowledge base tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("[*] Creating support knowledge base tables...")
    
    # Create support_category table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            icon VARCHAR(50),
            parent_id INTEGER,
            display_order INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES support_category(id)
        )
    ''')
    print("✓ Created support_category table")
    
    # Create support_article table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_article (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            problem_description TEXT NOT NULL,
            problem_keywords TEXT,
            solution_steps TEXT NOT NULL,
            category_id INTEGER,
            source VARCHAR(50) DEFAULT 'manual',
            source_url VARCHAR(500),
            times_used INTEGER DEFAULT 0,
            times_successful INTEGER DEFAULT 0,
            success_rate REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            verified_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES support_category(id),
            FOREIGN KEY (verified_by) REFERENCES user(id)
        )
    ''')
    print("✓ Created support_article table")
    
    # Create support_conversation table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id VARCHAR(100) NOT NULL UNIQUE,
            initial_query TEXT,
            last_message TEXT,
            message_count INTEGER DEFAULT 0,
            was_helpful BOOLEAN,
            resolution_type VARCHAR(50),
            escalated_to_ticket BOOLEAN DEFAULT 0,
            ticket_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES task(id)
        )
    ''')
    print("✓ Created support_conversation table")
    
    # Create indexes for better search performance
    indexes = [
        ("idx_support_article_keywords", "support_article", "problem_keywords"),
        ("idx_support_article_category", "support_article", "category_id"),
        ("idx_support_article_success", "support_article", "success_rate DESC"),
        ("idx_support_article_active", "support_article", "is_active"),
        ("idx_support_conversation_session", "support_conversation", "session_id"),
        ("idx_support_category_active", "support_category", "is_active"),
    ]
    
    for index_name, table_name, columns in indexes:
        try:
            cursor.execute(f'''
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON {table_name}({columns})
            ''')
        except Exception as e:
            # Index might already exist with different definition
            pass
    print("✓ Created performance indexes")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Support knowledge base tables created successfully!")

def add_default_categories():
    """Add some default support categories"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if categories already exist
    cursor.execute("SELECT COUNT(*) FROM support_category")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("[*] Adding default support categories...")
        
        categories = [
            ('Account & Login', 'Issues with logging in, passwords, and account access', 'fa-user-lock', 1),
            ('Technical Issues', 'Software bugs, errors, and technical problems', 'fa-bug', 2),
            ('Billing & Payments', 'Questions about invoices, payments, and subscriptions', 'fa-credit-card', 3),
            ('How To / Getting Started', 'Tutorials and guides for using features', 'fa-book-open', 4),
            ('Hardware & Devices', 'Issues with computers, printers, and peripherals', 'fa-desktop', 5),
            ('Network & Connectivity', 'Internet, WiFi, and connection problems', 'fa-wifi', 6),
            ('Other', 'General questions and miscellaneous issues', 'fa-question-circle', 99),
        ]
        
        for name, description, icon, order in categories:
            cursor.execute('''
                INSERT INTO support_category (name, description, icon, display_order)
                VALUES (?, ?, ?, ?)
            ''', (name, description, icon, order))
        
        conn.commit()
        print("✓ Added default categories")
    else:
        print("✓ Categories already exist, skipping...")
    
    conn.close()

def add_sample_articles():
    """Add some sample knowledge base articles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if articles already exist
    cursor.execute("SELECT COUNT(*) FROM support_article")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("[*] Adding sample knowledge base articles...")
        
        articles = [
            (
                'Cannot Login - Password Reset',
                'I forgot my password and cannot login to my account',
                'login,password,forgot,reset,access,locked',
                '''1. Go to the login page
2. Click "Forgot Password" link
3. Enter your email address
4. Check your email for the reset link
5. Click the link and create a new password
6. Try logging in with your new password

If you still cannot login, please submit a support ticket.''',
                1,  # Account & Login category
                'manual'
            ),
            (
                'Browser Not Loading Correctly',
                'The website is not displaying correctly or pages are not loading',
                'browser,loading,display,blank,white,error,page',
                '''1. Clear your browser cache and cookies
   - Chrome: Settings > Privacy > Clear browsing data
   - Firefox: Settings > Privacy > Clear Data
   
2. Try a different browser (Chrome, Firefox, Edge, Safari)

3. Disable browser extensions temporarily

4. Check your internet connection

5. Try accessing from a different device

If the problem persists, it may be a server issue. Please submit a ticket.''',
                2,  # Technical Issues category
                'manual'
            ),
            (
                'Printer Not Working',
                'My printer is not printing or is not detected by the computer',
                'printer,print,not working,offline,paper,jam',
                '''1. Check if the printer is turned on and connected
2. Ensure there is paper and ink/toner
3. Clear any paper jams
4. Restart the printer
5. On your computer:
   - Windows: Settings > Devices > Printers & Scanners
   - Mac: System Preferences > Printers & Scanners
6. Remove and re-add the printer
7. Update or reinstall printer drivers from manufacturer website

If still not working, try connecting via USB instead of WiFi.''',
                5,  # Hardware category
                'manual'
            ),
        ]
        
        for title, problem, keywords, solution, category_id, source in articles:
            cursor.execute('''
                INSERT INTO support_article 
                (title, problem_description, problem_keywords, solution_steps, category_id, source, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, 80.0)
            ''', (title, problem, keywords, solution, category_id, source))
        
        conn.commit()
        print("✓ Added sample articles")
    else:
        print("✓ Articles already exist, skipping...")
    
    conn.close()

def main():
    print("=" * 60)
    print("Support Knowledge Base Migration")
    print("=" * 60)
    
    # Check dependencies
    check_and_install_dependencies()
    
    # Create tables
    create_tables()
    
    # Add default data
    add_default_categories()
    add_sample_articles()
    
    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print("\nThe AI Support Assistant is now ready to use.")
    print("Access it at: /web/tickets/guest")
    print("\nFeatures:")
    print("  - Self-learning knowledge base")
    print("  - Web search for unknown issues")
    print("  - Automatic solution saving when marked helpful")
    print("=" * 60)

if __name__ == '__main__':
    main()
