import { useState } from "react";
import { users as initialUsers } from "../utils/data";

export default function Users() {
  const [users, setUsers] = useState(initialUsers);

  const handleRoleChange = (index, newRole) => {
    const updated = [...users];
    updated[index].role = newRole;

    // Simulated privilege creep risk
    updated[index].risk = newRole === "HR" ? 80 : 10;

    setUsers(updated);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Users</h2>

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
                    <div style={{ fontSize: "12px", color: "#555" }}>
                      Retained permissions from previous role
                    </div>
                  )}
                </td>

            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
