from emailing_system.extensions import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"

    uid = db.Column('UID', db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    employee_name = db.Column(db.String(100))
    email = db.Column(db.String(200))

    def __init__(self, id, name, email):
        self.employee_id = id
        self.employee_name = name
        self.email = email


class Events(db.Model):
    __tablename__ = "events"
    
    eid = db.Column('EID', db.Integer, primary_key = True)
    employee_id = db.Column(db.Integer)
    event_type = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def __init__(self, id, event_type, dt):
        self.employee_id = id
        self.event_type = event_type
        if type(dt)==str:
            self.date = datetime.strptime(dt, "%Y-%m-%d")
        else:    
            self.date = dt

class EmailTemplates(db.Model):
    __tablename__ = "email_templates"

    fid = db.Column('FID', db.Integer, primary_key = True)
    event_type = db.Column(db.String(100))
    email_template = db.Column(db.String(500))

    def __init__(self, event_type, email_template):
        self.email_template = email_template
        self.event_type = event_type

class EmailTracker(db.Model):
    __tablename__ = "email_tracker"

    tid = db.Column('TID', db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime)
    employee_id = db.Column(db.Integer)
    event_type = db.Column(db.String(100))
    email_content = db.Column(db.String(500))
    status = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, created_at, employee_id, event_type, email_content, status, description):
        self.created_at = created_at
        self.employee_id = employee_id
        self.event_type = event_type
        self.email_content = email_content
        self.status = status
        self.description = description

class Logs(db.Model):
    __tablename__ = "logs"

    lid = db.Column('LID', db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime)
    log_type = db.Column(db.String(100))
    log_text = db.Column(db.String(100))

    def __init__(self, created_at, log_type, log_text):
        self.created_at = created_at
        self.log_type = log_type
        self.log_text = log_text