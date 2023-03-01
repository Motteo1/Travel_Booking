"""
create test cases for all methods in engine.py
"""

from datetime import datetime
import unittest
import os
import json
import uuid
import hashlib
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from classes import storage
from classes.models import Base, User, Booking
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm import sessionmaker


Base.metadata.create_all(self.__engine)
Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
self.__session = Session()

def close(self):
        """close session"""
        self.__session.close()

def get(self, cls, id):
        """get object by id"""
        if cls and id:
                key = f'{cls}.{id}'
                if key in self.__objects:
                    return self.__objects[key]
        return None

def count(self, cls=None):
        """count number of objects in storage"""
        return len(self.all(cls)) if cls else len(self.all())