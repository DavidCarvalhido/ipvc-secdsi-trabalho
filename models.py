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

    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"))

    event_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)

    department = db.Column(db.String(100))
    criticality = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)


class Policy(db.Model):
    __tablename__ = "policies"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)
    #condition = db.Column(db.String(100), nullable=False)
    enabled = db.Column(db.Boolean, default=True)

    # condições
    department = db.Column(db.String(100))
    allowed_start_hour = db.Column(db.Integer)
    allowed_end_hour = db.Column(db.Integer)
    device_whitelist = db.Column(db.Text)
    # !condições

    probability = db.Column(db.Integer)
    impact = db.Column(db.Integer)
    confidentiality = db.Column(db.Integer)
    integrity = db.Column(db.Integer)
    availability = db.Column(db.Integer)

    asset_type = db.Column(db.String(50))
    minimum_criticality = db.Column(db.String(20))


class Control(db.Model):
    __tablename__ = "controls"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"))

    control_type = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)


class ComplianceResult(db.Model):
    __tablename__ = "compliance_results"

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"))
    control_id = db.Column(db.Integer, db.ForeignKey("controls.id"))

    compliant = db.Column(db.Boolean)
    reason = db.Column(db.Text)


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