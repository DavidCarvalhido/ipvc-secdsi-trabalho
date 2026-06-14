from models import Incident
from app import db
from datetime import datetime


# ISO 27001 Risk Matrix Engine
RISK_MATRIX = {
    "LOGIN_FAILED": {
        "probability": 3,
        "impact": 2,
        "cia": {"C": 1, "I": 1, "A": 2}
    },

    "USB_CONNECTED": {
        "probability": 4,
        "impact": 3,
        "cia": {"C": 3, "I": 2, "A": 3}
    },

    "FILE_DOWNLOAD": {
        "probability": 3,
        "impact": 4,
        "cia": {"C": 5, "I": 3, "A": 2}
    },

    "PRIVILEGE_CHANGE": {
        "probability": 2,
        "impact": 5,
        "cia": {"C": 5, "I": 5, "A": 3}
    }
}


def calculate_risk_score(probability, impact):
    return probability * impact


def classify_risk(score):
    if score <= 4:
        return "Low"
    elif score <= 9:
        return "Medium"
    elif score <= 16:
        return "High"
    else:
        return "Critical"
    

def evaluate_policy(policy):
    score = calculate_risk_score(policy.probability, policy.impact)

    return {
        "score": score,
        "risk_level": classify_risk(score),
        "cia": {
            "C": policy.confidentiality,
            "I": policy.integrity,
            "A": policy.availability
        }
    }


def evaluate_event(event):
    """
    Função principal do motor ISO 27001
    """

    event_type = event.event_type

    # default caso não exista regra
    rule = RISK_MATRIX.get(event_type, {
        "probability": 2,
        "impact": 2,
        "cia": {"C": 1, "I": 1, "A": 1}
    })

    probability = rule["probability"]
    impact = rule["impact"]

    score = calculate_risk_score(probability, impact)
    risk_level = classify_risk(score)

    cia = rule["cia"]

    return {
        "probability": probability,
        "impact": impact,
        "score": score,
        "risk_level": risk_level,
        "cia": cia
    }

# def calculate_risk(probability, impact):
#     score = probability * impact

#     if score <= 3:
#         return "Low"
#     elif score <= 6:
#         return "Medium"
#     elif score <= 9:
#         return "High"
#     else:
#         return "Critical"