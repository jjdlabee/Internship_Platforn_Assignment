import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
# from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 
staff_cli = AppGroup('staff', help='Staff object commands') 
student_cli = AppGroup('student', help='Student object commands')
employer_cli = AppGroup('employer', help='Employer object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("type", default="user")
def create_user_command(username, password, type):
    create_user(username, password, type)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())



@employer_cli.command("create_job", help="Creates a job for an employer")
@click.argument("employer_id", default=3)
@click.argument("title", default="Software Engineer")
@click.argument("description", default="Develop and maintain software applications.")
@click.argument("location", default="Remote")
@click.argument("salary", default=100000)
def create_job_command(employer_id, title, description, location, salary):
    if create_job_for_employer(employer_id, title, description, location, salary):
        print(f'Job "{title}" created for employer {employer_id}!')
    else:
        print(f'Failed to create job for employer {employer_id}.')

@employer_cli.command("list_jobs", help="Lists jobs for an employer")
@click.argument("employer_id", default=3)
def list_jobs_command(employer_id):
    jobs = get_jobs_for_employer(employer_id)
    if jobs is not None:
        print(jobs)
    else:
        print(f'No jobs found for employer {employer_id}.')
    return

@employer_cli.command("get_shortlist", help="Get the shortlist for a job")
@click.argument("employer_id", default=3)
@click.argument("job_id", default=1)
def get_shortlist_command(employer_id, job_id):
    job = get_job(job_id)
    if job is None:
        print(f'Job with ID {job_id} not found.')
        return
    shortlist = get_shortlisted_applicants(employer_id, job)
    if shortlist is not None:
        print(shortlist)
    else:
        print(f'No shortlist found for job {job_id}.')

@employer_cli.command("reply_applicant", help="Reply to an applicant for a job")
@click.argument("employer_id", default=3)
@click.argument("job_id", default=1)
@click.argument("student_id", default=2)
@click.argument("accept", default=True, type=bool)
def reply_applicant_command(employer_id, job_id, student_id, accept):
    job = get_job(job_id)
    student = get_student(student_id)
    if job is None:
        print(f'Job with ID {job_id} not found.')
        return
    if student is None:
        print(f'Student with ID {student_id} not found.')
        return
    result = reply_applicant(employer_id, job, student, accept)
    if result:
        decision = 'accepted' if accept else 'rejected'
        print(f'Applicant {student_id} has been {decision} for job {job_id}.')
    else:
        print(f'Failed to process the application for student {student_id} on job {job_id}.')



@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

@student_cli.command("toggle_availability", help="Toggle student availability")
@click.argument("student_id", default=2)
def toggle_availability_command(student_id):
    result = toggle_availability(student_id)
    if result:
        print(f'Student {student_id} availability toggled.')
    else:
        print(f'Student {student_id} not found.')
        
@student_cli.command("view_shortlist", help="View shortlisted internships for a student")
@click.argument("student_id", default=2)
def view_shortlist_command(student_id):
    internships = view_shortlisted_internships(student_id)
    if internships is not None:
        print(internships)
    else:
        print(f'No shortlisted internships found for student {student_id}.')

@student_cli.command("view_internship_status", help="View internship status for a student")
@click.argument("student_id", default=2)
@click.argument("job_id", default=1)
def view_internship_status_command(student_id, job_id):
    status = view_internship_status(student_id, job_id)
    if status is not None:
        print(status)
    else:
        print(f'No internship found for student {student_id} on job {job_id}.')

@staff_cli.command("list", help="Lists staff in the database")
@click.argument("format", default="string")
def list_staff_command(format):
    if format == 'string':
        print(get_all_staff())
    else:
        print(get_all_staff_json())
        
@staff_cli.command("list_students", help="Lists students assigned to a staff member")
@click.argument("staff_id", default=1)
def list_students_command(staff_id):
    students = get_students_by_staff_id(staff_id)
    if students is not None:
        print(students)
    else:
        print(f'No students found for staff member {staff_id}.')
        
@staff_cli.command("add_student", help="Assign a student to a staff member")
@click.argument("staff_id", default=1)
@click.argument("student_id", default=2)
def add_student_command(staff_id, student_id):
    student = get_student(student_id)
    if student is None:
        print(f'Student with ID {student_id} not found.')
        return
    result = add_student_to_staff(staff_id, student)
    if result:
        print(f'Student {student_id} added to staff member {staff_id}.')
    else:
        print(f'Failed to add student {student_id} to staff member {staff_id}.')
        
@staff_cli.command("add_shortlist", help="Add a student to a job shortlist")
@click.argument("staff_id", default=1)
@click.argument("student_id", default=2)
@click.argument("job_id", default=1)
def add_shortlist_command(staff_id, student_id, job_id):
    student = get_student(student_id)
    if student is None:
        print(f'Student with ID {student_id} not found.')
        return
    job = get_job(job_id)
    if job is None:
        print(f'Job with ID {job_id} not found.')
        return
    result = add_student_to_shortlist(staff_id, student, job)
    if result:
        print(f'Student {student_id} added to job {job_id} shortlist.')
    else:
        print(f'Failed to add student {student_id} to job {job_id} shortlist.')

app.cli.add_command(user_cli) # add the group to the cli
app.cli.add_command(staff_cli)
app.cli.add_command(student_cli)
app.cli.add_command(employer_cli)
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)