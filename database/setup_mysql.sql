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
DROP TABLE IF EXISTS 'flight';
DROP TABLE IF EXISTS 'hotel';
DROP TABLE IF EXISTS 'bus';

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
    (id, first_name, last_name, password, email, contact, payment_details)
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
    FOREIGN KEY (destination_id) REFERENCES destination(id),
    completed BOOLEAN
);
INSERT INTO booking
    (user_id, destination_id, flight_id, hotel_id, bus_id, date, amount, completed)

VALUES
    (0, "user_id", "destination_id", "flight_id", "hotel_id", "bus_id", "date", "amount");

CREATE TABLE
IF NOT EXISTS destination
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO destination
    (id, name, description)
VALUES
    (0, "name", "description");

CREATE TABLE
IF NOT EXISTS flight
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    departure VARCHAR(255) NOT NULL,
    arrival VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);
INSERT INTO flight
    (id, destination_id, departure, arrival, date, time, price)
VALUES
    (0, "destination_id", "departure", "arrival", "date", "time", "price");

CREATE TABLE
IF NOT EXISTS hotel
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);
INSERT INTO hotel
    (id, destination_id, name, description, price)
VALUES
    (0, "destination_id", "name", "description", "price");

CREATE TABLE
IF NOT EXISTS bus
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    departure VARCHAR(255) NOT NULL,
    arrival VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);
INSERT INTO bus
    (id, destination_id, departure, arrival, date, time, price)
VALUES
    (0, "destination_id", "departure", "arrival", "date", "time", "price");
