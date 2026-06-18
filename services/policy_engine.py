from models import User, Asset, Policy


def matches_policy(event, policy):
    # Event Type
    if event.event_type != policy.event_type:
        return False

    user = User.query.get(event.user_id)

    if not user:
        return False

    # Departament
    if (policy.department and user.department.lower() != policy.department.lower()):
        return False

    # Allowed Schedule
    if (policy.allowed_start_hour is not None and policy.allowed_end_hour is not None):
        if event.timestamp:
            event_hour = event.timestamp.hour
            
            if (event_hour < policy.allowed_start_hour or event_hour > policy.allowed_end_hour):
                return False
    
    asset = Asset.query.get(event.asset_id)

    if not asset:
        return False

    if (policy.asset_type and asset.asset_type != policy.asset_type):
        return False

    levels = {
        "Low":1,
        "Medium":2,
        "High":3,
        "Critical":4
    }

    if (policy.minimum_criticality):
        # if (levels[asset.criticality] < levels[policy.minimum_criticality]):
        #     return False
        asset_level = (levels.get(asset.criticality.lower(), 0))
        policy_level = (levels.get(policy.minimum_criticality.lower(), 0))

        if asset_level < policy_level:
            print("FAIL → criticality")

            return False

    return True


def find_policies(event):
    policies = Policy.query.filter_by(enabled=True).all()

    matches = []

    for policy in policies:
        if matches_policy(event, policy):
            matches.append(policy)

    return matches