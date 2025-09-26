from App.models import Staff
from App.database import db

def create_staff(username, password):
    newstaff = Staff(username=username, password=password)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def get_staff_by_username(username):
    result = db.session.execute(db.select(Staff).filter_by(username=username))
    return result.scalar_one_or_none()

def get_staff(id):
    return db.session.get(Staff, id)

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()

def get_all_staff_json():
    staffs = get_all_staff()
    if not staffs:
        return []
    staffs = [staff.get_json() for staff in staffs]
    return staffs

def update_staff(id, username):
    staff = get_staff(id)
    if staff:
        staff.username = username
        # staff is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def delete_staff(id):
    staff = get_staff(id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return True
    return None

def add_student_to_staff(staff_id, student):
    staff = get_staff(staff_id)
    if staff and student.availability and student not in staff.students:
        staff.students.append(student)
        db.session.commit()
        return True
    return None

def get_students_for_staff(id):
    staff = get_staff(id)
    if staff:
        return [student.get_json() for student in staff.students]
    return None

def remove_student_from_staff(staff_id, student):
    staff = get_staff(staff_id)
    if staff and student in staff.students:
        staff.students.remove(student)
        db.session.commit()
        return True
    return None

def add_student_to_shortlist(staff_id, student, job):
    staff = get_staff(staff_id)
    if staff and student in staff.students and job not in student.jobs:
        student.jobs.append(job)
        db.session.commit()
        return True
    return None

def remove_student_from_shortlist(staff_id, student, job):
    staff = get_staff(staff_id)
    if staff and student in staff.students and job in student.jobs:
        student.jobs.remove(job)
        db.session.commit()
        return True
    return None

def get_shortlisted_jobs_for_student(staff_id, student):
    staff = get_staff(staff_id)
    if staff and student in staff.students:
        return [job.get_json() for job in student.jobs]
    return None