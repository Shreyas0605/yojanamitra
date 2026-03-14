import sqlite3
import re

def clean_markdown(text):
    if not text or not isinstance(text, str):
        return text
    # Remove markdown artifacts like **, *, __, _, #, ~, ` often added by AI
    # We are careful not to remove normal punctuation.
    cleaned = re.sub(r'[\*\_#~`]+', '', text)
    # Also remove standalone '>' used for blockquotes if they appear as formatting
    cleaned = re.sub(r'^\s*>\s+', '', cleaned, flags=re.MULTILINE)
    # Clean up multiple spaces that might result from removal
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    return cleaned.strip()

def main():
    db_path = 'instance/yojanamitra.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, description, benefits, eligibility, exclusions, application_process, documents_required FROM scheme")
    except sqlite3.OperationalError as e:
        print(f"Error selecting from 'scheme': {e}")
        return
        
    rows = cursor.fetchall()
    
    updated_count = 0
    for row in rows:
        sch_id, name, desc, benefits, eligibility, exclusions, process, docs = row
        
        new_desc = clean_markdown(desc)
        new_benefits = clean_markdown(benefits)
        new_eligibility = clean_markdown(eligibility)
        new_exclusions = clean_markdown(exclusions)
        new_process = clean_markdown(process)
        new_docs = clean_markdown(docs)
        
        if (new_desc != desc or new_benefits != benefits or new_eligibility != eligibility or 
            new_exclusions != exclusions or new_process != process or new_docs != docs):
            
            cursor.execute("""
                UPDATE scheme 
                SET description = ?, benefits = ?, eligibility = ?, exclusions = ?, application_process = ?, documents_required = ?
                WHERE id = ?
            """, (new_desc, new_benefits, new_eligibility, new_exclusions, new_process, new_docs, sch_id))
            updated_count += 1

    conn.commit()
    conn.close()
    print(f"Total schemes cleaned of Markdown artifacts: {updated_count}")

if __name__ == "__main__":
    main()
