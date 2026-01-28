"""
Password Recovery Script
This script helps recover access to your account by resetting the password.
"""
import sqlite3
import sys
sys.path.insert(0, '.')

from app.core.security import get_password_hash

def list_users(db_path):
    """List all users in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # First check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables in database: {tables}")
    
    if 'user' not in tables:
        print("No 'user' table found in database!")
        conn.close()
        return []
    
    cursor.execute("SELECT id, username, email, is_admin FROM user")
    users = cursor.fetchall()
    conn.close()
    return users

def reset_password(db_path, user_id, new_password):
    """Reset password for a user"""
    hashed = get_password_hash(new_password)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET hashed_password = ? WHERE id = ?", (hashed, user_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    return rows_affected > 0

if __name__ == "__main__":
    # Check both database files
    print("=" * 50)
    print("Checking main database (data.db):")
    print("=" * 50)
    users = list_users("data.db")
    if users:
        print("\nUsers found:")
        for u in users:
            print(f"  ID: {u[0]}, Username: {u[1]}, Email: {u[2]}, Admin: {u[3]}")
    
    print("\n" + "=" * 50)
    print("Checking backup database (data.db.backup_test):")
    print("=" * 50)
    backup_users = list_users("data.db.backup_test")
    if backup_users:
        print("\nUsers found in backup:")
        for u in backup_users:
            print(f"  ID: {u[0]}, Username: {u[1]}, Email: {u[2]}, Admin: {u[3]}")
    
    # Offer to restore backup if main db is empty and backup has data
    if not users and backup_users:
        print("\n" + "=" * 50)
        print("Your main database is EMPTY but backup has data!")
        print("To restore from backup, run:")
        print("  copy data.db.backup_test data.db")
        print("=" * 50)
    
    # Interactive password reset
    if users or backup_users:
        print("\n" + "=" * 50)
        print("To reset a password, call this script with arguments:")
        print("  python recover_password.py <database_file> <user_id> <new_password>")
        print("Example:")
        print("  python recover_password.py data.db.backup_test 1 NewPassword123")
        print("=" * 50)
    
    # Handle command line arguments for password reset
    if len(sys.argv) == 4:
        db_file = sys.argv[1]
        user_id = int(sys.argv[2])
        new_password = sys.argv[3]
        
        if reset_password(db_file, user_id, new_password):
            print(f"\n✓ Password successfully reset for user ID {user_id}!")
        else:
            print(f"\n✗ Failed to reset password. User ID {user_id} not found.")
