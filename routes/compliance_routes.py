from flask import Blueprint, jsonify
from models import ComplianceResult, Policy, Control, Event


compliance_bp = Blueprint("compliance_bp", __name__)


# GET ALL COMPLIANCE RESULTS
@compliance_bp.route("/compliance-results", methods=["GET"])
def get_compliance_results():
    results = ComplianceResult.query.all()
    response = []

    for r in results:
        policy = Policy.query.get(r.policy_id)
        control = Control.query.get(r.control_id)
        event = Event.query.get(r.event_id)

        response.append({
            "id": r.id,
            "event_id": r.event_id,
            "event_type":
                event.event_type
                if event
                else None,
            "policy":
                policy.name
                if policy
                else None,
            "control":
                control.name
                if control
                else None,
            "compliant": r.compliant,
            "reason": r.reason
        })

    return jsonify(
        response
    ), 200


# GET SINGLE RESULT
@compliance_bp.route("/compliance-results/<int:id>", methods=["GET"])
def get_compliance_result(id):
    r = ComplianceResult.query.get_or_404(id)
    policy = Policy.query.get(r.policy_id)
    control = Control.query.get(r.control_id)
    event = Event.query.get(r.event_id)

    return jsonify({
        "id": r.id,
        "event_id": r.event_id,
        "event_type":
            event.event_type
            if event
            else None,
        "policy":
            policy.name
            if policy
            else None,
        "control":
            control.name
            if control
            else None,
        "compliant": r.compliant,
        "reason": r.reason
    }), 200