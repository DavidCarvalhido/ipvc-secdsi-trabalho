#from app import db
from database import db
print("DB MODELS:", id(db))
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50))
    department = db.Column(db.String(50))


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    event_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    severity = db.Column(db.String(20))
    risk_level = db.Column(db.String(20))
    probability = db.Column(db.Integer)
    impact = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class RiskAssessment(db.Model):
    __tablename__ = "risk_assessments"

    id = db.Column(db.Integer, primary_key=True)

    incident_id = db.Column(db.Integer, db.ForeignKey("incidents.id"))

    probability = db.Column(db.Integer)
    impact = db.Column(db.Integer)
    risk_score = db.Column(db.Integer)
    risk_level = db.Column(db.String(20))

    confidentiality = db.Column(db.Integer)
    integrity = db.Column(db.Integer)
    availability = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)