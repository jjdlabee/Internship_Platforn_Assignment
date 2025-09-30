from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer,  db.ForeignKey('user.id'), unique=True, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    availability = db.Column(db.Boolean, default=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, availability=False):
        super().__init__(username, password, 'student')
        self.availability = availability

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'staff_id': self.staff_id,
            'type': self.type,
            'availability': self.availability
        }

