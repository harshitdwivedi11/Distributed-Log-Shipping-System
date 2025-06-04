CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id VARCHAR(50),
    message VARCHAR(255),
    level VARCHAR(50),
    created_at DATETIME,
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP
);