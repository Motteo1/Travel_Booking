#!/usr/bin/python3
"""Database for Storage"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src.classes.models import Base, User, Booking
Base = declarative_base()

class DBStorage:
    """Database storage class"""
    __slots__ = ['__engine', '__metadata', '__session']

    def __init__(self):
        """Create engine and link to database"""
        user = "root"
        pwd = "root"
        host = "localhost"
        db = "booking"
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}?charset=utf8mb4', pool_pre_ping=True)
        self.__metadata = MetaData()
        self.__metadata.reflect(bind=self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def save(self, obj):  # sourcery skip: do-not-use-bare-except
        """Save changes to database"""
        try:
            self.__session.add(obj)
            self.__session.commit()
        except:
            self.__session.rollback()
    
    def new(self, obj):  # sourcery skip: do-not-use-bare-except
        """Add object to database"""
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
            key = f"{obj.__class__.__name__}.{obj.id}"
            booking_dict[key] = obj
        return booking_dict
    
    def count(self):
        """Count number of objects in database"""
        return sum(1 for _ in self.__session.query(Booking).all())
    
    def get_booking_by_id(self, booking_id):
        """Get booking by id"""
        try:
            return self.__session.query(Booking).filter_by(id=booking_id).first()
        except(IndexError, TypeError):
            return None
    
    def get_booking_by_user_id(self, user_id):
        # sourcery skip: inline-immediately-returned-variable
        """Get booking by user id"""
        try:
            obj = self.__session.query(Booking).filter_by(user_id=user_id).all()
            return obj
        except(IndexError, TypeError):
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by id"""
        try:
            return self.__session.query(User).filter_by(id=user_id).first()
        except TypeError:
            print('Error at engine.get_user_by_id X___X')
            return None
    
    def get_user_by_email(self, email):
        # sourcery skip: inline-immediately-returned-variable
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
