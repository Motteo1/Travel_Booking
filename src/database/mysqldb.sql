-- prepare a dataabase with sample data in datadase
-- Grant usage on *.* to 'booking'@'localhost';

CREATE DATABASE 
IF NOT EXISTS booking;
USE booking;
GRANT ALL PRIVILEGES ON booking.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE
IF NOT EXISTS user
(
    id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    payment_details VARCHAR(255) NOT NULL
);

INSERT INTO user 
    (first_name, last_name, password, email, contact, payment_details)
VALUES 
    ("first_name", "last_name", "password", "email", "contact", "payment_details");

CREATE TABLE
IF NOT EXISTS destination
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL
);

INSERT INTO destination
    (name, description)
VALUES
    ("name", "description");

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
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);

INSERT INTO flight
    (destination_id, departure, arrival, date, time, price)
VALUES
    (1, "departure", "arrival", "2023-03-01", "12:00:00", 500);

CREATE TABLE
IF NOT EXISTS hotel
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);

INSERT INTO hotel
    (destination_id, name, description, price)
VALUES
    (1, "name", "description", 500);

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
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);

INSERT INTO bus
    (destination_id, departure, arrival, date, time, price)
VALUES
    (1, "departure", "arrival", "2023-03-01", "12:00:00", 500);

CREATE TABLE
IF NOT EXISTS booking
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    destination_id INT NOT NULL,
    flight_id INT NOT NULL,
    hotel_id INT NOT NULL,
    bus_id INT NOT NULL,
    date DATE NOT NULL,
    amount INT NOT NULL,
    completed BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);

INSERT INTO booking
    (user_id, destination_id, flight_id, hotel_id, bus_id, date, amount, completed)
VALUES
    ("user_id", "destination_id", "flight_id", "hotel_id", "bus_id", "date", "amount", false);

CREATE TABLE
IF NOT EXISTS payment
(
    id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    booking_id INT NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES booking(id)
);
INSERT INTO payment
    (user_id, booking_id, amount)
VALUES
    ("user_id", "booking_id", "amount");