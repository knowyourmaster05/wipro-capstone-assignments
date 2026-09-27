CREATE DATABASE IF NOT EXISTS api_automation_db;
USE api_automation_db;

CREATE TABLE IF NOT EXISTS user_management (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  password VARCHAR(100),
  title VARCHAR(10),
  birth_date VARCHAR(5),
  birth_month VARCHAR(15),
  birth_year VARCHAR(5),
  firstname VARCHAR(100),
  lastname VARCHAR(100),
  company VARCHAR(150),
  address1 VARCHAR(255),
  address2 VARCHAR(255),
  country VARCHAR(100),
  zipcode VARCHAR(20),
  state VARCHAR(100),
  city VARCHAR(100),
  mobile_number VARCHAR(20),
  api_response_id VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
