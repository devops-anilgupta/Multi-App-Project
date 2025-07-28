USE userdb;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  resume_path VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email, resume_path) VALUES
  ('John Doe', 'john@example.com', '/resumes/john_doe.pdf'),
  ('Jane Smith', 'jane@example.com', '/resumes/jane_smith.pdf'),
  ('Robert Brown', 'robert@example.com', '/resumes/robert_brown.pdf'),
  ('Emily White', 'emily@example.com', '/resumes/emily_white.pdf'),
  ('Michael Green', 'michael@example.com', '/resumes/michael_green.pdf');