import json
import os
import sqlite3
import sys
import urllib
from urllib2 import Request, urlopen, URLError

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User of the Films to Friends website."""

    def __init__(self, email=None, password=None, fname=None, lname=None, zipcode=None, personality=None):
        self.email = email
        self.set_password(password)
        self.fname = fname
        self.lname = lname
        self.zipcode = zipcode
        self.personality = personality

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    pw_hash = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    personality = db.Column(db.String(64), nullable=True)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s email=%s>" % (self.user_id, self.email)



###############################################################

def get_db_cursor():
    """Return a database cursor"""
    mypath = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(mypath, "filmstofriends.db"))
    cursor = conn.cursor()
    return cursor

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    dbpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filmstofriends.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dbpath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # bug fix for SQLAlchemy misbehaving on Apache servers
    db.app = app 
    db.init_app(app)
    # ensure that the databases are created for each context
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
