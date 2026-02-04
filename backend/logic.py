
role_permissions = {
    "Developer": ["deploy", "read_repo", "write_code"],
    "HR": ["view_employee", "edit_payroll"],
    "Admin": ["all_access"]
}

def derive_permissions(role):
    return role_permissions.get(role, [])

def detect_creep(current, allowed):
    return list(set(current) - set(allowed))

def risk_score(extra_permissions):
    return len(extra_permissions) * 25

ROLE_PERMISSIONS = {
    "Developer": {"deploy", "read_repo", "write_code"},
    "HR": {"view_employee", "edit_payroll"},
    "Admin": {"deploy", "read_repo", "write_code", "view_employee", "edit_payroll"}
}

def derive_permissions(role):
    return ROLE_PERMISSIONS.get(role, set())

def detect_privilege_creep(current_permissions, new_role):
    allowed = derive_permissions(new_role)
    extra = set(current_permissions) - allowed
    return list(extra)

def risk_score(extra_permissions):
    return min(len(extra_permissions) * 30, 100)

def explain(extra_permissions):
    if not extra_permissions:
        return "No excess permissions detected."
    return f"User retains permissions {extra_permissions} from previous role."

