CREATE DATABASE hubspace;
USE hubspace;

CREATE TABLE pcs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pc_number VARCHAR(10) NOT NULL,
    category ENUM('Gaming', 'Study') NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    specs VARCHAR(255) NOT NULL
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    category ENUM('Gaming', 'Study') NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    pc_number VARCHAR(10) NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pc_number VARCHAR(50) NOT NULL,
    items TEXT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
