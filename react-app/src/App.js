import UserForm from './UserForm'; // Adjust path if UserForm.js is in another folder
import React from "react";

function App() {
  return (
    <div>
      <h1>Hello from React!</h1>
      <hr/>
      <p>Welcome to the React application.</p>
      <p>This application allows you to upload your resume.</p>
      <p>Make sure to fill out the form correctly.</p>
      <p>Check the console for any errors during submission.</p>
      <p>Ensure your backend is running on port 5000.</p>
      <p>For any issues, refer to the documentation or contact support.</p>
      <p>Thank you for using our application!</p>
      <hr/>
      <p>Below is the user form for uploading your resume:</p>
      <hr/>
      <h1>Upload Your Resume</h1>
      <UserForm />
      <p>Make sure to fill out the form correctly.</p>
      <p>Check the console for any errors during submission.</p>
      <p>Ensure your backend is running on port 5000.</p>
      <p>For any issues, refer to the documentation or contact support.</p>
      <p>Thank you for using our application!</p>
    </div>
  );
}

export default App;
