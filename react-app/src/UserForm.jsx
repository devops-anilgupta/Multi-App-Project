import React, { useState } from 'react';

function UserForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [resume, setResume] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('resume', resume);

    const response = await fetch('http://localhost:5000/api/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    alert(result.message);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" placeholder="Name" required onChange={(e) => setName(e.target.value)} />
      <input type="email" name="email" placeholder="Email" required onChange={(e) => setEmail(e.target.value)} />
      <input type="file" name="resume" accept=".pdf,.doc,.docx" required onChange={(e) => setResume(e.target.files[0])} />
      <button type="submit">Submit</button>
    </form>
  );
}

export default UserForm;
