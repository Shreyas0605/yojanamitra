"""
Add new certificate number fields to User table
"""
import sqlite3

# Connect to database (Flask uses instance folder)
conn = sqlite3.connect('instance/yojanamitra.db')
cursor = conn.cursor()

try:
    # Add new columns
    cursor.execute('ALTER TABLE user ADD COLUMN ration_card_number VARCHAR(100)')
    print("[OK] Added ration_card_number column")
except sqlite3.OperationalError as e:
    print(f"[SKIP] ration_card_number: {e}")

try:
    cursor.execute('ALTER TABLE user ADD COLUMN caste_cert_no VARCHAR(100)')
    print("[OK] Added caste_cert_no column")
except sqlite3.OperationalError as e:
    print(f"[SKIP] caste_cert_no: {e}")

try:
    cursor.execute('ALTER TABLE user ADD COLUMN income_cert_no VARCHAR(100)')
    print("[OK] Added income_cert_no column")
except sqlite3.OperationalError as e:
    print(f"[SKIP] income_cert_no: {e}")

# Commit and close
conn.commit()
conn.close()

print("\n[SUCCESS] Database migration complete!")
