from .user import create_user
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'staff')
    create_user('alice', 'alicepass', 'student')
    create_user('charlie', 'charliepass', 'employer', "Charlie's Company")
