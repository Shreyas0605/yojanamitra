"""
Document Encryption Utility
Handles encryption/decryption of sensitive user documents
"""

from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentEncryption:
    def __init__(self):
        # Get encryption key from environment
        key = os.getenv('DOCUMENT_ENCRYPTION_KEY')
        
        if not key:
            print("WARNING: DOCUMENT_ENCRYPTION_KEY not set in .env")
            print("Generating a new key for development...")
            key = Fernet.generate_key().decode()
            print(f"Add this to your .env file:\nDOCUMENT_ENCRYPTION_KEY={key}")
            
        # Convert string key to bytes if needed
        if isinstance(key, str):
            key = key.encode()
            
        self.cipher = Fernet(key)
    
    def encrypt_file(self, file_path):
        """
        Encrypt a file in place
        Returns: True if successful, False otherwise
        """
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt data
            encrypted_data = self.cipher.encrypt(data)
            
            # Write encrypted data back
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"[OK] Encrypted: {file_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Encryption failed for {file_path}: {e}")
            return False
    
    def decrypt_file(self, file_path):
        """
        Decrypt a file and return the decrypted data (in memory)
        Does NOT modify the file on disk
        Returns: decrypted bytes or None
        """
        try:
            # Read encrypted file
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            return decrypted_data
            
        except Exception as e:
            print(f"[ERROR] Decryption failed for {file_path}: {e}")
            return None
    
    def is_encrypted(self, file_path):
        """
        Check if a file is encrypted by attempting to decrypt it
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            self.cipher.decrypt(data)
            return True
        except:
            return False

# Global instance
encryptor = DocumentEncryption()

def generate_new_key():
    """
    Generate a new encryption key for initial setup
    """
    key = Fernet.generate_key()
    print("\n" + "="*60)
    print("NEW ENCRYPTION KEY GENERATED")
    print("="*60)
    print("\nAdd this line to your .env file:")
    print(f"\nDOCUMENT_ENCRYPTION_KEY={key.decode()}")
    print("\nIMPORTANT: Keep this key secure and never commit it to git!")
    print("="*60 + "\n")
    return key.decode()

if __name__ == "__main__":
    # Generate key if run directly
    generate_new_key()
