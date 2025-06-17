-- Drop tables if they exist (use with caution in production)
DROP TABLE IF EXISTS verified_users;
DROP TABLE IF EXISTS otps;
DROP TABLE IF EXISTS emails;

-- Table for registered Algopath emails
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Table to store OTPs
CREATE TABLE IF NOT EXISTS otps (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to track verified users
CREATE TABLE IF NOT EXISTS verified_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_id BIGINT UNIQUE NOT NULL
);

-- Insert dummy emails
INSERT INTO emails (email) VALUES
('tashu1938@gmail.com'), 
('user@gmail.com'),
('soniayush312@gmail.com'),
('231162@iiitt.ac.in');
