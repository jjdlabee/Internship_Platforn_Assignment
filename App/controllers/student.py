from App.models import Student
from App.database import db


def create_student(username, password):
    newstudent = Student(username=username, password=password)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def get_student_by_username(username):
    result = db.session.execute(db.select(Student).filter_by(username=username))
    return result.scalar_one_or_none()

def get_student(id):
    return db.session.get(Student, id)

def get_all_student():
    return db.session.scalars(db.select(Student)).all()

def get_all_student_json():
    students = get_all_student()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        # student is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def toggle_availability(id):
    student = get_student(id)
    if student:
        student.availability = not student.availability
        db.session.commit()
        return True
    return None

def view_shortlisted_internships(id):
    student = get_student(id)
    if student:
        return [internship.get_json() for internship in student.jobs]
    return None

def delete_student(id):
    student = get_student(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return True
    return None

