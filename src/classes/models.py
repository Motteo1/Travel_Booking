#!/usr/bin/python3
from datetime import date
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src import login_user
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.session import object_session
from flask_login import UserMixin



Base = declarative_base()


def find_user(user_id):  # sourcery skip: do-not-use-bare-except
    try:
        user = User.query.get(user_id)
    except:
        user = None
    return user

class User(Base, UserMixin):
    """Class User is a blueprint to create user objects"""

    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    contact = Column(String(128), nullable=False)
    bookings = relationship('Booking', backref='user', cascade='all, delete')
    payments = relationship('Payment', backref='user', cascade='all, delete')
        
    
    def __init__(self, *args, **kwargs):
        """Instantiates user object"""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.password = ""
        self.contact = ""

        for k, v in kwargs.items():
            if k == 'password':
                User.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password):
        """Hashes password"""
        secure_pw = generate_password_hash(password)
        setattr(self, 'password', secure_pw)
    
    def __check_password(self, password):
        """
        Checks password hash against password entered by user at login time
        returns True or False if they match or not respectively
        """
        return check_password_hash(self.password, password)



class Booking(Base):
    """Class Booking is a blueprint to create booking objects"""

    __tablename__ = 'bookings'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    destination_id = Column(Integer, ForeignKey('destinations.id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flights.id'), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=False)
    dates_id = Column(Integer, ForeignKey('dates.id'), nullable=False)
    payments = relationship('Payment', backref='booking', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates booking object"""
        self.user_id = ""
        self.destination_id = ""
        self.flight_id = ""
        self.hotel_id = ""
        self.bus_id = ""
        self.dates_id = ""
        self.payments = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class Dates(Base):
    """Class Dates is a blueprint to create dates objects"""

    __tablename__ = 'dates'

    id = Column(Integer, nullable=False, primary_key=True)
    departure_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    bookings = relationship('Booking', backref='dates', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates dates object"""
        self.departure_date = ""
        self.return_date = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class Destination(Base):
    """Class Destination is a blueprint to create destination objects"""

    __tablename__ = 'destinations'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    bookings = relationship('Booking', backref='destination', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates destination object"""
        self.name = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class Payment(Base):
    """Class Payment is a blueprint to create payment objects"""

    __tablename__ = 'payments'

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates payment object"""
        self.user_id = ""
        self.booking_id = ""
        self.amount = ""
        self.date = ""

        for k, v in kwargs.items():
            setattr(self, k, v)
    
class Flight(Base):
    """Class Flight is a blueprint to create flight objects"""

    __tablename__ = 'flights'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    bookings = relationship('Booking', backref='flight', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates flight object"""
        self.name = ""
        self.price = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class Hotel(Base):
    """Class Hotel is a blueprint to create hotel objects"""

    __tablename__ = 'hotels'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    bookings = relationship('Booking', backref='hotel', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates hotel object"""
        self.name = ""
        self.price = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class Bus(Base):
    """Class Bus is a blueprint to create bus objects"""

    __tablename__ = 'buses'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    bookings = relationship('Booking', backref='bus', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """Instantiates bus object"""
        self.name = ""
        self.price = ""

        for k, v in kwargs.items():
            setattr(self, k, v)
