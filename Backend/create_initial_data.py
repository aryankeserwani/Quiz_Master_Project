from flask import current_app as app
from Backend.models import db, User, Role, Subject, Chapter
from flask_security import hash_password
import uuid
from datetime import datetime, timedelta

# Function to create initial data
def create_initial_data():
    # Check if data already exists
    user_count = User.query.count()
    if user_count == 0:
        # Create roles
        admin_role = Role(name='Admin', description='Administrator with full access')
        user_role = Role(name='user', description='Regular user with limited access')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        
        # Create admin user
        admin = User(
            username='admin',
            password=hash_password('admin123'),
            email='admin@example.com',
            full_name='Administrator',
            qualification='Admin',
            dob=datetime.now().date() - timedelta(days=365*25),  # Example DOB - 25 years ago
            active=True,
            roles=[admin_role],
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(admin)
        
        # Create a demo user
        demo_user = User(
            username='user',
            password=hash_password('user123'),
            email='user@example.com',
            full_name='Demo User',
            qualification='Student',
            dob=datetime.now().date() - timedelta(days=365*20),  # Example DOB - 20 years ago
            active=True,
            roles=[user_role],
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(demo_user)
        
        # Create sample subjects
        subjects = [
            Subject(name='Mathematics', description='Study of numbers, quantities, and shapes'),
            Subject(name='Science', description='Systematic study of the structure and behavior of the physical and natural world'),
            Subject(name='Computer Science', description='Study of computers and computational systems')
        ]
        db.session.add_all(subjects)
        db.session.commit()
        
        # Create sample chapters for each subject
        math_chapters = [
            Chapter(name='Algebra', description='Study of mathematical symbols and the rules for manipulating these symbols', subject_id=1),
            Chapter(name='Calculus', description='Study of continuous change and motion', subject_id=1),
            Chapter(name='Geometry', description='Study of shapes, sizes, positions, and dimensions', subject_id=1)
        ]
        
        science_chapters = [
            Chapter(name='Physics', description='Study of matter, energy, and their interactions', subject_id=2),
            Chapter(name='Chemistry', description='Study of substances and their interactions', subject_id=2),
            Chapter(name='Biology', description='Study of living organisms', subject_id=2)
        ]
        
        cs_chapters = [
            Chapter(name='Programming', description='Process of designing and building an executable computer program', subject_id=3),
            Chapter(name='Data Structures', description='Data organization, management, and storage format', subject_id=3),
            Chapter(name='Algorithms', description='Step-by-step procedure for calculations or problem-solving', subject_id=3)
        ]
        
        db.session.add_all(math_chapters + science_chapters + cs_chapters)
        db.session.commit()
        
        print("Initial data created successfully.")
    else:
        print("Data already exists. Skipping creation of initial data.")

# Call the function
with app.app_context():
    create_initial_data()
    
    