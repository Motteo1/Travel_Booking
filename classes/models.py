#!/usr/bin/python3
from datetime import date
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session


Base = declarative_base()

@login_user.user_loader
def find_user(user_id):
    return storage.get_user_by_id(user_id)

class User(Base):
    """Class User is a blueprint to create user objects"""

    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    contact = Column(String(128), nullable=False)
    bookings = relationship('Booking', backref='user', cascade='all, delete')
    
    
    
    
    def __init__(self, *args, **kwargs):
        """Instantiates user object"""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.password = ""
        self.contact = ""

        for k, v in kwargs.items():
            if k is 'password':
                User.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password):
        """Hashes password"""
        self.password = bcrypt.generate_password_hash(password)



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
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates booking object"""
        self.user_id = ""
        self.destination_id = ""
        self.flight_id = ""
        self.hotel_id = ""
        self.bus_id = ""
        self.dates_id = ""

        for k, v in kwargs.items():
            setattr(self, k, v)