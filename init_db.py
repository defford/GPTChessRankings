from app import create_app, db
from app.models import User, Player

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('admin_password')  # Change this to a secure password
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        print("Database initialized.")

if __name__ == '__main__':
    init_db()