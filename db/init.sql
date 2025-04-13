CREATE DATABASE IF NOT EXISTS messages_db;
USE messages_db;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a user with appropriate permissions
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON messages_db.* TO 'user'@'%';
FLUSH PRIVILEGES;
