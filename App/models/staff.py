from App.database import db
from App.models import User

class Staff(User):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, unique=True)
    students = db.relationship('Student', backref='staff', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }
    
    def __init__(self, username, password, staff_id):
        super().__init__(username, password)
        self.staff_id = staff_id

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'staff_id': self.staff_id,
            'type': self.type,
            'students': [student.get_json() for student in self.students]
        }

# class Staff(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username =  db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(256), nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#     students = db.relationship('Student', backref='staff', lazy=True)

#     def __init__(self, username, password):
#         self.username = username
#         self.set_password(password)

#     def get_json(self):
#         return{
#             'id': self.id,
#             'username': self.username,
#             'name': self.name,
#             'students': [student.get_json() for student in self.students]
#         }

#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password)
    
#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)