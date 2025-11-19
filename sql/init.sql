-- Create the assignment4-504 database
CREATE DATABASE IF NOT EXISTS `assignment4-504`;
USE `assignment4-504`;

-- Create the visits table
CREATE TABLE IF NOT EXISTS `visits` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `patient_id` INT NOT NULL,
    `visit_date` DATETIME NOT NULL,
    `bp_sys` INT,
    `bp_dia` INT
);

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON `assignment4-504`.* TO 'root'@'%';
FLUSH PRIVILEGES;



