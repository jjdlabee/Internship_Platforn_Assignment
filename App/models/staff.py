from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    available_students = db.relationship('Student', backref='staff', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'available_students': [student.get_json() for student in self.available_students]
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)