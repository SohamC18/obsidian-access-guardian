from fastapi import FastAPI
from backend.logic import derive_permissions, detect_creep, risk_score

def get_effective_permissions(user):
    # Zero Trust: never trust stored permissions blindly
    return derive_permissions(user["role"])


app = FastAPI()

users = [
    {
        "name": "Rahul",
        "role": "Developer",
        "permissions": ["deploy", "read_repo", "write_code"],
        "risk_score": 0,
        "explanation": "No risk yet"
    }
]
# privilege history timeline
timeline = []
# live alert storage
alerts = []



@app.get("/")
def home():
    return {"message": "Obsidian Backend Running"}

@app.get("/users")
def get_users():
    response = []

    for user in users:
        effective = get_effective_permissions(user)

        response.append({
            "name": user["name"],
            "role": user["role"],
            "effective_permissions": effective,
            "risk_score": user.get("risk_score", 0),
            "explanation": user.get("explanation", "")
        })

    return response


@app.post("/change-role")
def change_role(name: str, new_role: str):

    for user in users:
        if user["name"] == name:

            # derive allowed permissions
            allowed = derive_permissions(new_role)
            current = user["permissions"]

            # detect privilege creep
            extra = detect_creep(current, allowed)
            score = risk_score(extra)

            # generate explanation (AI-style reasoning)
            if extra:
                explanation = f"User retained {extra} after role change to {new_role}"
            else:
                explanation = "No privilege creep detected"

            # update user state automatically
            user["role"] = new_role
            user["risk_score"] = score
            user["explanation"] = explanation

            from datetime import datetime

            # store timeline entry
            timeline.append({
                "name": name,
                "old_role": user["role"],
                "new_role": new_role,
                "extra_permissions": extra,
                "risk_score": score,
                "explanation": explanation,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # create live alert if risk is high
            if score >= 70:
                alerts.append({
                    "name": name,
                    "risk_score": score,
                    "message": f"High risk detected for {name}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })



            return {
                "user": name,
                "new_role": new_role,
                "risk_score": score,
                "explanation": explanation
            }

    return {"error": "User not found"}


@app.post("/simulate-attack")
def simulate_attack():
    # Force Rahul to have developer permissions
    users[0]["role"] = "Developer"
    users[0]["permissions"] = ["deploy", "read_repo", "write_code"]

    # Now simulate role change to HR
    new_role = "HR"

    allowed = derive_permissions(new_role)
    current = users[0]["permissions"]

    extra = detect_creep(current, allowed)
    score = risk_score(extra)

    users[0]["role"] = new_role

    return {
        "message": "Privilege creep simulated",
        "extra_permissions": extra,
        "risk_score": score
    }

@app.get("/risk-summary")
def risk_summary():

    high = []
    medium = []
    low = []

    for user in users:
        score = user.get("risk_score", 0)

        if score >= 70:
            high.append(user["name"])
        elif score >= 30:
            medium.append(user["name"])
        else:
            low.append(user["name"])

    return {
        "total_users": len(users),
        "high_risk_users": high,
        "medium_risk_users": medium,
        "safe_users": low
    }
@app.get("/timeline")
def get_timeline():
    return timeline
@app.get("/alerts")
def get_alerts():
    return alerts

@app.get("/check-access")
def check_access(name: str, permission: str):

    for user in users:
        if user["name"] == name:
            effective = get_effective_permissions(user)

            if permission in effective:
                return {
                    "access": "allowed",
                    "reason": "Permission derived from current role"
                }
            else:
                return {
                    "access": "denied",
                    "reason": "Zero-trust engine blocked access"
                }

    return {"error": "User not found"}
