from App.database import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=True)
    shortlist = db.relationship('Staff', secondary='internship', backref=db.backref('jobs', lazy=True))

    def __init__(self, title, description, location, salary=None):
        self.title = title
        self.description = description
        self.location = location
        self.salary = salary

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'salary': self.salary
        }