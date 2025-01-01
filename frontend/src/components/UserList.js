import React, { useEffect, useState } from "react";
import axios from "../api/axios";

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get("/users")
      .then(response => setUsers(response.data))
      .catch(error => console.error("Error fetching users:", error));
  }, []);

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.name} - Borrowed Books: {user.borrowed_books}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;