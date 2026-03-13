import sqlite3
import html
import re

def clean_text(text):
    if not text or not isinstance(text, str):
        return text
    # Decode HTML entities (e.g., &amp;quot; -> ")
    # Sometimes it's double encoded, so we unescape twice if needed
    cleaned = html.unescape(text)
    cleaned = html.unescape(cleaned)
    
    # Remove excessive symbols or weird artifacts
    # (Optional: can add more rules here if needed)
    
    return cleaned.strip()

def main():
    db_path = 'instance/yojanamitra.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Correct table name for Scheme model is 'scheme'
    try:
        cursor.execute("SELECT id, name, description, benefits, eligibility, exclusions, application_process, documents_required FROM scheme")
    except sqlite3.OperationalError as e:
        print(f"Error selecting from 'scheme': {e}")
        return
        
    rows = cursor.fetchall()
    
    updated_count = 0
    for row in rows:
        sch_id, name, desc, benefits, eligibility, exclusions, process, docs = row
        
        new_desc = clean_text(desc)
        new_benefits = clean_text(benefits)
        new_eligibility = clean_text(eligibility)
        new_exclusions = clean_text(exclusions)
        new_process = clean_text(process)
        new_docs = clean_text(docs)
        
        if (new_desc != desc or new_benefits != benefits or new_eligibility != eligibility or 
            new_exclusions != exclusions or new_process != process or new_docs != docs):
            
            cursor.execute("""
                UPDATE scheme 
                SET description = ?, benefits = ?, eligibility = ?, exclusions = ?, application_process = ?, documents_required = ?
                WHERE id = ?
            """, (new_desc, new_benefits, new_eligibility, new_exclusions, new_process, new_docs, sch_id))
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"Cleaned {updated_count} schemes...")

    conn.commit()
    conn.close()
    print(f"Total schemes cleaned: {updated_count}")

if __name__ == "__main__":
    main()
