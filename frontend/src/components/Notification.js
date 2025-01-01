import React, { useEffect, useState } from "react";
import axios from "../api/axios";

function Notification() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    axios.get("/notifications")
      .then(response => setNotifications(response.data.notifications))
      .catch(error => console.error("Error fetching notifications:", error));
  }, []);

  return (
    <div>
      <h2>Notifications</h2>
      <p>{notifications}</p>
    </div>
  );
}

export default Notification;