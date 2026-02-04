import { useState } from "react";
import { users as initialUsers } from "../utils/data";
import axios from "axios";


export default function Users() {
  const [users, setUsers] = useState(initialUsers);

  const handleRoleChange = async (index, newRole) => {
  const user = users[index];

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/change-role",
      null,
      {
        params: {
          name: user.name,
          new_role: newRole,
        },
      }
    );

    const updated = [...users];
    updated[index] = {
      ...user,
      role: newRole,
      risk: response.data.risk_score,
    };

    setUsers(updated);
  } catch (err) {
    console.error("Backend error", err);
  }
};

const fixAccess = (index) => {
  const updated = [...users];
  updated[index].risk = 0;
  setUsers(updated);
};

  return (
    <div style={{ padding: "24px" }}>
      <h2 style={{ color: "#c7d2fe", marginBottom: "16px" }}>
  Users & Access Risk
</h2>
<button
  onClick={async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/simulate-attack"
    );
    alert("Privilege creep simulated!");
  }}
  style={{
    marginBottom: "16px",
    padding: "6px 12px",
    backgroundColor: "#7c3aed",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  }}
>
  Simulate Privilege Creep
</button>


      <table border="1" cellPadding="10" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
            <th>Risk Score</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u, i) => (
            <tr key={i}>
              <td>{u.name}</td>

              <td>
                <select
                  value={u.role}
                  onChange={(e) =>
                    handleRoleChange(i, e.target.value)
                  }
                >
                  <option value="Developer">Developer</option>
                  <option value="HR">HR</option>
                  <option value="Admin">Admin</option>
                </select>
              </td>

              <td>
  <span style={{ color: u.risk > 50 ? "red" : "green" }}>
    {u.risk}
  </span>

  {u.risk > 50 && (
    <>
      <div style={{ fontSize: "12px", color: "#555" }}>
        Retained permissions from previous role
      </div>

      <button
        onClick={() => fixAccess(i)}
        style={{
          marginTop: "6px",
          padding: "4px 8px",
          fontSize: "12px",
          cursor: "pointer"
        }}
      >
        Fix Access
      </button>
    </>
  )}
</td>


            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
