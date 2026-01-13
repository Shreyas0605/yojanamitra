from app import app, SchemeTranslation

with app.app_context():
    t = SchemeTranslation.query.first()
    if t:
        print(f"✅ Translation Found (Lang: {t.language})")
        data = t.to_dict()
        print(f"Name (Parsed): {data.get('name')}")
        print(f"Content Sample: {str(t.content_json)[:100]}...")
    else:
        print("❌ No translations found in database.")
