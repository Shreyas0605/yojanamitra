from app import app, db, User

with app.app_context():
    email = "06052004shreyas2@gmail.com"
    user = User.query.filter_by(email=email).first()
    
    if user:
        print(f"Current: {user.name}")
        user.name = "Shreyas"
        db.session.commit()
        print(f"Updated to: {user.name} ✅")
    else:
        print("User not found.")
