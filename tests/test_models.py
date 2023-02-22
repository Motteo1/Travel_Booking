"""
create test cases for all methods in models.py
"""
# from classes.models import User, Booking, Destination, Date, Payment
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# import unittest
# import os
# import json
# import uuid
# import hashlib
# import app
# from werkzeug.security import generate_password_hash, check_password_hash
# from classes import storage
#
# class TestModels(unittest.TestCase):
#     """Test models"""
#     def setUp(self):
#         """Create test cases for all methods in models.py"""
#         Base.metadata.create_all(self.__engine)
#         Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
#         self.__session = Session()
#
#     def close(self):
#         """close session"""
#         self.__session.close()
#
#     def get(self, cls, id):
#         """get object by id"""
#         if cls and id:
#             key = cls + '.' + id
#             if key in self.__objects:
#                 return self.__objects[key]
#         return None
#
#     def count(self, cls=None):
#         """count number of objects in storage"""
#         if cls:
#             return len(self.all(cls))
#         return len(self.all())
#
#     def test_user(self):
#         """test user class"""
#         user = User()
#         self.assertEqual(user.id, str(uuid.uuid4()))
#         self.assertEqual(user.created_at, datetime.now())
#         self.assertEqual(user.updated_at, datetime.now())
#         self.assertEqual(user.first_name, "")
#         self.assertEqual(user.last_name, "")
#         self.assertEqual(user.email, "")
#         self.assertEqual(user.password, "")
#         self.assertEqual(user.phone, "")
#         self.assertEqual(user.address, "")
#         self.assertEqual(user.city, "")
#         self.assertEqual(user.state, "")
#         self.assertEqual(user.zipcode, "")
#         self.assertEqual(user.country, "")
#         self.assertEqual(user.is_admin, False)
#         self.assertEqual(user.is_active, True)
#         self.assertEqual(user.is_anonymous, False)
#         self.assertEqual(user.get_id(), user.id)
#         self.assertEqual(user.to_dict(), {
#             'id': user.id,
#             'created_at': user.created_at,
#             'updated_at': user.updated_at,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#             'password': user.password,
#             'phone': user.phone,
#             'address': user.address,
#             'city': user.city,
#             'state': user.state,
#             'zipcode': user.zipcode,
#             'country': user.country,
#             'is_admin': user.is_admin,
#             'is_active': user.is_active,
#             'is_anonymous': user.is_anonymous
#         })
#         self.assertEqual(user.__repr__(), "<User {}>".format(user.id))
#         self.assertEqual(user.__str__(), user.id)
#         self.assertEqual(user.__class__.__name__, "User")
#         self.assertEqual(user.__class__.__tablename__, "users")
#         self.assertEqual(user.__class__.__table_args__, {'extend_existing': True})
#         self.assertEqual(user.__class__.__mapper_args__, {'polymorphic_identity': 'user'})
#         self.assertEqual(user.__class__.__mapper__.polymorphic_on, user.type)
#         self.assertEqual(user.__class__.__mapper__.polymorphic_identity, 'user')
#         self.assertEqual(user.__class__.__mapper__.inherits, None)
#         self.assertEqual(user.__class__.__mapper__.local_table, user.__class__.__table__)
#         self.assertEqual(user.__class__.__mapper__.primary_key, [user.id])
#         self.assertEqual(user.__class__.__mapper__.version_id_col, None)

#     def test_booking(self):
#         """test booking class"""
#         booking = Booking()
#         self.assertEqual(booking.id, str(uuid.uuid4()))
#         self.assertEqual(booking.created_at, datetime.now())
#         self.assertEqual(booking.updated_at, datetime.now())
#         self.assertEqual(booking.user_id, "")
#         self.assertEqual(booking.destination_id, "")
#         self.assertEqual(booking.date_id, "")
#         self.assertEqual(booking.payment_id, "")
#         self.assertEqual(booking.to_dict(), {
#             'id': booking.id,
#             'created_at': booking.created_at,
#             'updated_at': booking.updated_at,
#             'user_id': booking.user_id,
#             'destination_id': booking.destination_id,
#             'date_id': booking.date_id,
#             'payment_id': booking.payment_id
#         })
#         self.assertEqual(booking.__repr__(), "<Booking {}>".format(booking.id))
#         self.assertEqual(booking.__str__(), booking.id)
#         self.assertEqual(booking.__class__.__name__, "Booking")
#         self.assertEqual(booking.__class__.__tablename__, "bookings")
#         self.assertEqual(booking.__class__.__table_args__, {'extend_existing': True})
#         self.assertEqual(booking.__class__.__mapper_args__, {'polymorphic_identity': 'booking'})
#         self.assertEqual(booking.__class__.__mapper__.polymorphic_on, booking.type)
#         self.assertEqual(booking.__class__.__mapper__.polymorphic_identity, 'booking')
#         self.assertEqual(booking.__class__.__mapper__.inherits, None)
#         self.assertEqual(booking.__class__.__mapper__.local_table, booking.__class__.__table__)
#         self.assertEqual(booking.__class__.__mapper__.primary_key, [booking.id])
#         self.assertEqual(booking.__class__.__mapper__.version_id_col, None)
#

#     def test_destination(self):
#         """test destination class"""
#         destination = Destination()
#         self.assertEqual(destination.id, str(uuid.uuid4()))
#         self.assertEqual(destination.created_at, datetime.now())
#         self.assertEqual(destination.updated_at, datetime.now())
#         self.assertEqual(destination.name, "")
#         self.assertEqual(destination.description, "")
#         self.assertEqual(destination.price, 0)
#         self.assertEqual(destination.to_dict(), {
#             'id': destination.id,
#             'created_at': destination.created_at,
#             'updated_at': destination.updated_at,
#             'name': destination.name,
#             'description': destination.description,
#             'price': destination.price
#         })
#         self.assertEqual(destination.__repr__(), "<Destination {}>".format(destination.id))
#         self.assertEqual(destination.__str__(), destination.id)

#     def test_date(self):
#         """test date class"""
#         date = Date()
#         self.assertEqual(date.id, str(uuid.uuid4()))
#         self.assertEqual(date.created_at, datetime.now())
#         self.assertEqual(date.updated_at, datetime.now())
#         self.assertEqual(date.date, "")
#         self.assertEqual(date.to_dict(), {
#             'id': date.id,
#             'created_at': date.created_at,
#             'updated_at': date.updated_at,
#             'date': date.date
#         })
#         self.assertEqual(date.__repr__(), "<Date {}>".format(date.id))
#         self.assertEqual(date.__str__(), date.id)

#     def test_payment(self):
#         """test payment class"""
#         payment = Payment()
#         self.assertEqual(payment.id, str(uuid.uuid4()))
#         self.assertEqual(payment.created_at, datetime.now())
#         self.assertEqual(payment.updated_at, datetime.now())
#         self.assertEqual(payment.amount, 0)
#         self.assertEqual(payment.to_dict(), {
#             'id': payment.id,
#             'created_at': payment.created_at,
#             'updated_at': payment.updated_at,
#             'amount': payment.amount
#         })
#         self.assertEqual(payment.__repr__(), "<Payment {}>".format(payment.id))
#         self.assertEqual(payment.__str__(), payment.id)

#     def test_review(self):
#         """test review class"""
#         review = Review()
#         self.assertEqual(review.id, str(uuid.uuid4()))
#         self.assertEqual(review.created_at, datetime.now())
#         self.assertEqual(review.updated_at, datetime.now())
#         self.assertEqual(review.user_id, "")
#         self.assertEqual(review.destination_id, "")
#         self.assertEqual(review.text, "")
#         self.assertEqual(review.to_dict(), {
#             'id': review.id,
#             'created_at': review.created_at,
#             'updated_at': review.updated_at,
#             'user_id': review.user_id,
#             'destination_id': review.destination_id,
#             'text': review.text
#         })
#         self.assertEqual(review.__repr__(), "<Review {}>".format(review.id))
#         self.assertEqual(review.__str__(), review.id)

#     def test_user(self):
#         """test user class"""
#         user = User()
#         self.assertEqual(user.id, str(uuid.uuid4()))
#         self.assertEqual(user.created_at, datetime.now())
#         self.assertEqual(user.updated_at, datetime.now())
#         self.assertEqual(user.email, "")
#         self.assertEqual(user.password, "")
#         self.assertEqual(user.first_name, "")
#         self.assertEqual(user.last_name, "")
#         self.assertEqual(user.to_dict(), {
#             'id': user.id,
#             'created_at': user.created_at,
#             'updated_at': user.updated_at,
#             'email': user.email,
#             'password': user.password,
#             'first_name': user.first_name,
#             'last_name': user.last_name
#         })
#         self.assertEqual(user.__repr__(), "<User {}>".format(user.id))
#         self.assertEqual(user.__str__(), user.id)

#     def test_base_model(self):
#         """test base model class"""
#         base_model = BaseModel()
#         self.assertEqual(base_model.id, str(uuid.uuid4()))
#         self.assertEqual(base_model.created_at, datetime.now())
#         self.assertEqual(base_model.updated_at, datetime.now())
#         self.assertEqual(base_model.to_dict(), {
#             'id': base_model.id,
#             'created_at': base_model.created_at,
#             'updated_at': base_model.updated_at
#         })
#         self.assertEqual(base_model.__repr__(), "<BaseModel {}>".format(base_model.id))
#         self.assertEqual(base_model.__str__(), base_model.id)

# if __name__ == '__main__':
#     unittest.main()

# #!/usr/bin/python3