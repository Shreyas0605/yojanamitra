from app import app, db, Scheme, SchemeTranslation
import json

with app.app_context():
    db.create_all()
    print("✅ Database tables verified/created.")
    
    # Check if we have any schemes to test translation on
    scheme = Scheme.query.first()
    if scheme:
        print(f"🔍 Found test scheme: {scheme.name} (ID: {scheme.id})")
        # Ensure it has some text
        if not scheme.benefits:
            scheme.benefits = "Test benefits for scheme"
            db.session.commit()
            print("📝 Added test benefits content.")
    else:
        print("⚠️ No schemes found in database to test translation.")
