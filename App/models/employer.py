from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models import User

class Employer(User):
    __tablename__ = 'employer'
    employer_id = db.Column(db.Integer, unique=True)
    company = db.Column(db.String(100), nullable=False)
    jobs = db.relationship('Job', backref='employer', lazy=True)    

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, employer_id, company):
        super().__init__(username, password)
        self.employer_id = employer_id
        self.company = company

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'employer_id': self.employer_id,
            'type': self.type,
            'jobs': [job.get_json() for job in self.jobs]
        }

