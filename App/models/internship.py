from App.database import db

class Internship(db.Model):
    __tablename__ = 'internship'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # e.g., pending, approved, completed

    def __init__(self, student_id, job_id, start_date, end_date, status='pending'):
        self.student_id = student_id
        self.job_id = job_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'job_id': self.job_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status
        }