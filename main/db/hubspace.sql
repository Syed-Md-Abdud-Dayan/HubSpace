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

INSERT INTO pcs (pc_number, category, is_available, specs) VALUES
('ALPHA1', 'Gaming', TRUE, 'Intel Core i7, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA2', 'Gaming', TRUE, 'Intel Core i7, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA3', 'Gaming', TRUE, 'AMD Ryzen 7, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA4', 'Gaming', TRUE, 'AMD Ryzen 7, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA5', 'Gaming', TRUE, 'Intel Core i5, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA6', 'Gaming', TRUE, 'Intel Core i5, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA7', 'Gaming', TRUE, 'AMD Ryzen 5, RTX 4060, 16GB RAM, 1TB SSD'),
('ALPHA8', 'Gaming', TRUE, 'AMD Ryzen 5, RTX 4060, 16GB RAM, 1TB SSD'),

('BETA1', 'Study', TRUE, 'Intel Core i5, Integrated Graphics, 8GB RAM, 512GB SSD'),
('BETA2', 'Study', TRUE, 'Intel Core i5, Integrated Graphics, 8GB RAM, 512GB SSD'),
('BETA3', 'Study', TRUE, 'Intel Core i5, Integrated Graphics, 16GB RAM, 512GB SSD'),
('BETA4', 'Study', TRUE, 'Intel Core i5, Integrated Graphics, 16GB RAM, 512GB SSD'),
('BETA5', 'Study', TRUE, 'AMD Ryzen 5, Integrated Graphics, 8GB RAM, 512GB SSD'),
('BETA6', 'Study', TRUE, 'AMD Ryzen 5, Integrated Graphics, 8GB RAM, 512GB SSD'),
('BETA7', 'Study', TRUE, 'AMD Ryzen 5, Integrated Graphics, 16GB RAM, 512GB SSD'),
('BETA8', 'Study', TRUE, 'AMD Ryzen 5, Integrated Graphics, 16GB RAM, 512GB SSD');
