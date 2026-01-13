import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('instance/yojanamitra.db')
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM scheme_translation")
        count = cursor.fetchone()[0]
        print(f"Total rows in scheme_translation: {count}")
        
        if count > 0:
            cursor.execute("SELECT content_json FROM scheme_translation LIMIT 1")
            print(f"Sample data: {cursor.fetchone()[0][:100]}...")
            
        conn.close()
    except Exception as e:
        print(f"Error accessing DB directly: {e}")

if __name__ == "__main__":
    check_db()
