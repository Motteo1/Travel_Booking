-- prepare a dataabase with sample data in datadase
-- Grant usage on *.* to 'booking'@'localhost';

import mysql.connector
from mysql.connector import Error
import warnings
from datetime import datetime, date, time, timedelta
import dateutil.parser
import pytz

# create a connection to the MySQL server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=localhost,
            user=root,
            passwd=3AnXdGtYpdvrsQ7!
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# create a cursor object to execute SQL commands
mycursor = mydb.cursor()

# execute the SQL commands to create the database and tables
mycursor.execute("CREATE DATABASE IF NOT EXISTS booking")
mycursor.execute("USE booking")
mycursor.execute("GRANT ALL PRIVILEGES ON booking.* TO 'root'@'localhost'")
mycursor.execute("FLUSH PRIVILEGES")
mycursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost'")
mycursor.execute("FLUSH PRIVILEGES")
mycursor.execute("""CREATE TABLE IF NOT EXISTS user
                    (
                        id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        contact VARCHAR(255) NOT NULL,
                        payment_details VARCHAR(255) NOT NULL
                    )""")
mycursor.execute("""INSERT INTO user 
                    (first_name, last_name, password, email, contact, payment_details)
                    VALUES 
                    ("first_name", "last_name", "password", "email", "contact", "payment_details")""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS destination
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description VARCHAR(255) NOT NULL
                    )""")
mycursor.execute("""INSERT INTO destination
                    (name, description)
                    VALUES
                    ("name", "description")""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS flight
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        destination_id INT NOT NULL,
                        departure VARCHAR(255) NOT NULL,
                        arrival VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        price INT NOT NULL,
                        FOREIGN KEY (destination_id) REFERENCES destination(id)
                    )""")
mycursor.execute("""INSERT INTO flight
                    (destination_id, departure, arrival, date, time, price)
                    VALUES
                    (1, "departure", "arrival", "2023-03-01", "12:00:00", 500)""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS hotel
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        destination_id INT NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        description VARCHAR(255) NOT NULL,
                        price INT NOT NULL,
                        FOREIGN KEY (destination_id) REFERENCES destination(id)
                    )""")
mycursor.execute("""INSERT INTO hotel
                    (destination_id, name, description, price)
                    VALUES
                    (1, "name", "description", 500)""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS bus
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        destination_id INT NOT NULL,
                        departure VARCHAR(255) NOT NULL,
                        arrival VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        price INT NOT NULL,
                        FOREIGN KEY (destination_id) REFERENCES destination(id)
                    )""")
mycursor.execute("""INSERT INTO bus
                    (destination_id, departure, arrival, date, time, price)
                    VALUES
                    (1, "departure", "arrival", "2023-03-01", "12:00:00", 500)""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS booking
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        destination_id INT NOT NULL,
                        flight_id INT NOT NULL,
                        hotel_id INT NOT NULL,
                        bus_id INT NOT NULL,
                        date DATE NOT NULL,
                        amount INT NOT NULL,
                        completed BOOLEAN,
                        FOREIGN KEY (user_id) REFERENCES user(id),
                        FOREIGN KEY (destination_id) REFERENCES destination(id)
                    )""")
mycursor.execute("""INSERT INTO booking
                    (destination_id, flight_id, hotel_id, bus_id, date, amount, completed)
                    VALUES
                    (1, 1, 1, 1, "2023-03-01", 500, 0)""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS payment
                    (
                        id INT UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        booking_id INT NOT NULL,
                        amount INT NOT NULL,
                        FOREIGN KEY (booking_id) REFERENCES booking(id)
                    )""")
mycursor.execute("""INSERT INTO payment
                    (user_id, booking_id, amount)
                    VALUES
                    (1, 1, 500)""")