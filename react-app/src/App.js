import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({ name: "", email: "", resume: null });
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);

  const handleChange = e => {
    const { name, value, files } = e.target;
    if (name === "resume") {
      setForm(prev => ({ ...prev, resume: files[0] }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/users`);
      setUsers(res.data);
    } catch (err) {
      console.error("Failed to fetch users", err);
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!form.resume) {
      setMessage("Please upload a resume file");
      return;
    }

    const formData = new FormData();
    formData.append("name", form.name);
    formData.append("email", form.email);
    formData.append("resume", form.resume);

    try {
      const res = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/api/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(res.data.message || "Upload successful!");
      setForm({ name: "", email: "", resume: null });  // reset form
      fetchUsers(); // fetch updated user list
    } catch (err) {
      setMessage("Upload failed");
    }
  };

  useEffect(() => {
    fetchUsers(); // fetch on first load
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: "auto", paddingTop: 50 }}>
      <h2>User Upload Form</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          onChange={handleChange}
          value={form.name}
          required
        />
        <br /><br />
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          value={form.email}
          required
        />
        <br /><br />
        <input
          type="file"
          name="resume"
          accept=".pdf"
          onChange={handleChange}
          required
        />
        <br /><br />
        <button type="submit">Submit</button>
      </form>
      <p>{message}</p>

      <h3>Uploaded Users</h3>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Resume Path</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.resume_path}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
