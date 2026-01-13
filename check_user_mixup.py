from app import app, User

with app.app_context():
    email = "06052004shreyas2@gmail.com" # Checking the one from the logs likely
    user = User.query.filter_by(email=email).first()
    if user:
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        print(f"ID: {user.id}")
    else:
        print(f"User {email} not found.")

    # Also check the other one if relevant
    email2 = "06052004shreyas@gmail.com"
    user2 = User.query.filter_by(email=email2).first()
    if user2:
        print(f"Email: {user2.email}")
        print(f"Name: {user2.name}")
        print(f"ID: {user2.id}")
