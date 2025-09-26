from App.models import Employer, Job
from App.database import db

def create_employer(username, password, company):
    newemployer = Employer(username=username, password=password, company=company)
    db.session.add(newemployer)
    db.session.commit()
    return newemployer

def get_employer_by_username(username):
    result = db.session.execute(db.select(Employer).filter_by(username=username))
    return result.scalar_one_or_none()

def get_employer(id):
    return db.session.get(Employer, id)

def get_all_employers():
    return db.session.scalars(db.select(Employer)).all()

def get_all_employers_json():
    employers = get_all_employers()
    if not employers:
        return []
    employers = [employer.get_json() for employer in employers]
    return employers

def update_employer(id, username, company):
    employer = get_employer(id)
    if employer:
        employer.username = username
        employer.company = company
        # employer is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def delete_employer(id):
    employer = get_employer(id)
    if employer:
        db.session.delete(employer)
        db.session.commit()
        return True
    return None

def create_job_for_employer(employer_id, title, description, location, salary=None):
    employer = get_employer(employer_id)
    if employer:
        newjob = Job(title=title, description=description, location=location, salary=salary)
        employer.jobs.append(newjob)
        db.session.add(newjob)
        db.session.commit()
        return newjob
    return None

def get_jobs_for_employer(id):
    employer = get_employer(id)
    if employer:
        return [job.get_json() for job in employer.jobs]
    return None

def reply_applicant(employer_id, job, student, accept=True):
    employer = get_employer(employer_id)
    if employer and job in employer.jobs and student in job.shortlist:
        if accept:
            job.shortlist.intership.decision = 'accepted'
            pass
        else:
            
            job.shortlist.intership.decision = 'rejected'
            job.shortlist.remove(student)
        db.session.commit()
        return True
    return None

def remove_job(employer_id, job):
    employer = get_employer(employer_id)
    if employer and job in employer.jobs:
        db.session.delete(job)
        db.session.commit()
        return True
    return None

def get_shortlisted_applicants(employer_id, job):
    employer = get_employer(employer_id)
    if employer and job in employer.jobs:
        return [student.get_json() for student in job.shortlist]
    return None

