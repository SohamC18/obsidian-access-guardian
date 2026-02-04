from fastapi import FastAPI
from backend.logic import derive_permissions, detect_creep, risk_score


app = FastAPI()

users = [
    {
        "name": "Rahul",
        "role": "Developer",
        "permissions": ["deploy", "read_repo", "write_code"]
    }
]

@app.get("/")
def home():
    return {"message": "Obsidian Backend Running"}

@app.get("/users")
def get_users():
    return users

@app.post("/change-role")
def change_role(name: str, new_role: str):

    for user in users:
        if user["name"] == name:

            allowed = derive_permissions(new_role)
            current = user["permissions"]

            extra = detect_creep(current, allowed)
            score = risk_score(extra)

            user["role"] = new_role

            return {
                "user": name,
                "new_role": new_role,
                "extra_permissions": extra,
                "risk_score": score
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
