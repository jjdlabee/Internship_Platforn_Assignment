from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    jobs = db.relationship('Job', backref='employer', lazy=True)

    def __init__(self, username, password, company):
        self.username = username
        self.company = company
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'company': self.company
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)