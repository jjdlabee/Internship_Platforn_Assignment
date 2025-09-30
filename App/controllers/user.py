from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password, type, company_name=None):
    if (type not in ['student', 'employer', 'staff']):
        raise ValueError("Invalid user type. Must be 'student', 'employer', or 'staff'.")
    elif (type == 'student'):
        newuser = Student(username=username, password=password)
    elif (type == 'employer'):
        newuser = Employer(username=username, password=password, company=company_name)
    elif (type == 'staff'):
        newuser = Staff(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        
        db.session.commit()
        return True
    return None

