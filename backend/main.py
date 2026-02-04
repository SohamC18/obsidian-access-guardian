from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic import (
    derive_permissions,
    detect_privilege_creep,
    risk_score,
    explain,
)

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------ In-memory users ------------------

users = [
    {
        "name": "Rahul",
        "role": "Developer",
        "permissions": ["deploy", "read_repo", "write_code"],
    }
]

# ------------------ Basic routes ------------------

@app.get("/")
def home():
    return {"message": "Obsidian Backend Running"}

@app.get("/users")
def get_users():
    return users

# ------------------ Role change analysis ------------------

@app.post("/change-role")
def change_role(name: str, new_role: str):
    for user in users:
        if user["name"] == name:
            allowed = derive_permissions(new_role)
            current = user["permissions"]

            extra = detect_privilege_creep(current, new_role)
            score = risk_score(extra)

            user["role"] = new_role

            return {
                "user": name,
                "new_role": new_role,
                "extra_permissions": extra,
                "risk_score": score,
                "explanation": explain(extra),
            }

    return {"error": "User not found"}

# ------------------ Simulate privilege creep ------------------

@app.post("/simulate-attack")
def simulate_attack():
    users[0]["role"] = "Developer"
    users[0]["permissions"] = ["deploy", "read_repo", "write_code"]

    new_role = "HR"
    current = users[0]["permissions"]

    extra = detect_privilege_creep(current, new_role)
    score = risk_score(extra)

    users[0]["role"] = new_role

    return {
        "message": "Privilege creep simulated",
        "extra_permissions": extra,
        "risk_score": score,
        "explanation": explain(extra),
    }

# ------------------ AI analysis endpoint ------------------

@app.post("/analyze")
def analyze_access(data: dict):
    current_permissions = data["current_permissions"]
    new_role = data["new_role"]

    extra = detect_privilege_creep(current_permissions, new_role)

    return {
        "extra_permissions": extra,
        "risk": risk_score(extra),
        "explanation": explain(extra),
    }
