from app import app, db
from sqlalchemy import text

with app.app_context():
    # Only drop the translation table to preserve other data
    print("🗑️ Dropping SchemeTranslation table...")
    try:
        db.session.execute(text('DROP TABLE scheme_translation'))
        db.session.commit()
        print("✅ Table dropped.")
    except Exception as e:
        print(f"⚠️ Drop failed (might not exist): {e}")

    print("🔨 Recreating tables...")
    db.create_all()
    print("✅ Schema updated successfully.")
