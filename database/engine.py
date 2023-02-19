#!/usr/bin/python3
"""Database for Storage"""
from classes.models import Base, User, Booking, Destination, Date, Payment
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and link to database"""
        user = "root"
        pwd = "root"
        host = "localhost"
        db = "booking"
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db), pool_pre_ping=True)
        self.__metadata = MetaData(bind=self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def save(self, obj):
        """Save changes to database"""
        try:
            self.__session.add(obj)
            self.__session.commit()
        except:
            self.__session.rollback()
        
    def delete(self, obj=None):
        """Delete object from database"""
        self.__session.delete(obj)
        self.__session.commit()
        self.__session.flush()
    
    def all(self, cls=None):
        """Return all booking objects from database"""
        booking_dict = {}
        for obj in self.__session.query(Booking).all():
            key = obj.__class__.__name__ + "." + obj.id
            booking_dict[key] = obj
        return booking_dict

        """Return all destination objects from database"""
        destination_dict = {}
        for obj in self.__session.query(Destination).all():
            key = obj.__class__.__name__ + "." + obj.id
            destination_dict[key] = obj
        return destination_dict

        """Return all payment objects from database"""
        payment_dict = {}
        for obj in self.__session.query(Payment).all():
            key = obj.__class__.__name__ + "." + obj.id
            payment_dict[key] = obj
        return payment_dict
    
    def count(self):
        """Count number of objects in database"""
        total = 0
        for obj in self.__session.query(Booking).all():
            total += 1
        return total
    
    def get_booking_by_id(self, booking_id):
        """Get booking by id"""
        try:
            obj = self.__session.query(Booking).filter_by(id=booking_id).first()
            return obj
        except(IndexError, TypeError):
            return None
    
    def get_booking_by_user_id(self, user_id):
        """Get booking by user id"""
        try:
            obj = self.__session.query(Booking).filter_by(user_id=user_id).all()
            return obj
        except(IndexError, TypeError):
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by id"""
        try:
            obj = self.__session.query(User).filter_by(id=user_id).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_id X___X')
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            obj = self.__session.query(User).filter_by(email=email).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_email X___X')
            return None
    
    def reload(self):
        """create all tables in database & session from engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine, 
                expire_on_commit=False))
    
    def close(self):
        """Calls remove() on private session attribute (self.__session)"""
        self.__session.close()