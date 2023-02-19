-- prepare a dataabase with sample data in datadase
-- Grant usage on *.* to 'booking'@'localhost';

CREATE DATABASE 
IF NOT EXISTS booking
-- CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '';
USE booking;
GRANT ALL PRIVILEGES ON booking.* TO 'root'@'localhost';
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

USE booking;
DROP TABLE IF EXISTS `booking`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS 'destination';

CREATE TABLE
IF NOT EXISTS user
(
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    payment_details VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO user 
    (first_name, last_name, password, email, contact) 
VALUES 
    (0, "first_name", "last_name", "password", "email", "contact", "payment_details");


CREATE TABLE
IF NOT EXISTS booking
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    destination_id VARCHAR(255) NOT NULL,
    flight_id INT NOT NULL,
    hotel_id INT NOT NULL,
    bus_id INT NOT NULL,
    date DATE NOT NULL,
    amount INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);
INSERT INTO booking
    (user_id, destination_id, flight_id, hotel_id, bus_id, date)

VALUES
    (0, "user_id", "destination_id", "flight_id", "hotel_id", "bus_id", "date", "amount");