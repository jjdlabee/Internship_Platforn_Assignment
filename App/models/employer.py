from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models import User

class Employer(User):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    jobs = db.relationship('Job', backref='employer', lazy=True)    

    __mapper_args__ = {
        'polymorphic_identity': 'employer',  
    }

    def __init__(self, username, password, company):
        super().__init__(username, password, 'employer')
        self.company = company

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'company': self.company,
            'type': self.type,
            'jobs': [job.get_json() for job in self.jobs]
        }

