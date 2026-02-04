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
