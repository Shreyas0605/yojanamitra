"""
Inactive User Cleanup Script
Deletes documents for users who haven't logged in for 30+ days
Run this script daily via cron job or task scheduler
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, UserDocument
from document_encryption import encryptor

def cleanup_inactive_user_documents():
    """
    Delete documents for users who haven't logged in for 30+ days
    """
    with app.app_context():
        # Calculate cutoff date (30 days ago)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        print(f"\n{'='*60}")
        print(f"INACTIVE USER DOCUMENT CLEANUP")
        print(f"{'='*60}")
        print(f"Cutoff Date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"(Deleting documents for users inactive since this date)\n")
        
        # Find users who haven't logged in for 30+ days
        inactive_users = User.query.filter(
            User.last_login < cutoff_date
        ).all()
        
        if not inactive_users:
            print("[INFO] No inactive users found. All users are active!")
            return
        
        print(f"[INFO] Found {len(inactive_users)} inactive users\n")
        
        total_docs_deleted = 0
        total_files_deleted = 0
        
        for user in inactive_users:
            # Get user's documents
            documents = UserDocument.query.filter_by(user_id=user.id).all()
            
            if not documents:
                continue
            
            print(f"\n[USER] {user.name} ({user.email})")
            print(f"       Last Login: {user.last_login.strftime('%Y-%m-%d') if user.last_login else 'Never'}")
            print(f"       Documents: {len(documents)}")
            
            for doc in documents:
                try:
                    # Delete file from disk
                    file_path = os.path.join('static/uploads/documents', doc.filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        total_files_deleted += 1
                        print(f"       [OK] Deleted file: {doc.filename}")
                    
                    # Delete database record
                    db.session.delete(doc)
                    total_docs_deleted += 1
                    
                except Exception as e:
                    print(f"       [ERROR] Failed to delete {doc.filename}: {e}")
            
            # Commit changes for this user
            db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"CLEANUP SUMMARY")
        print(f"{'='*60}")
        print(f"Inactive Users: {len(inactive_users)}")
        print(f"Documents Deleted (DB): {total_docs_deleted}")
        print(f"Files Deleted (Disk): {total_files_deleted}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    cleanup_inactive_user_documents()
