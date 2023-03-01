#!/usr/bin/python3
"""
HELPER METHODS
    logged_in:      Returns True if user is logged in. If not, redirects to login page.
    get_user_by_id: Returns user object by id.
    get_user_by_email: Returns user object by email.
    get_booking_by_id: Returns booking object by id.
    get_booking_by_user_id: Returns booking object by user id.
    get_destination_by_id: Returns destination object by id.
    get_flight_by_id: Returns flight object by id.
    get_hotel_by_id: Returns hotel object by id.
    get_payment_by_id: Returns payment object by id.
    get_payment_by_user_id: Returns payment object by user id.
    get_payment_by_booking_id: Returns payment object by booking id.
    is_booking_valid: Returns True if booking is valid. If not, returns False.
    email_confirm_trip: Sends email to user confirming trip.
    email_cancel_trip: Sends email to user cancelling trip.
    skip_hotel: Returns True if hotel is not required. If not, returns False.
    skip_flight: Returns True if flight is not required. If not, returns False.
    skip_bus: Returns True if bus is not required. If not, returns False.

"""
from datetime import date, datetime
from flask import Flask
from flask_mail import Mail, Message
from flask_login import current_user
import os
from src import app
from threading import Thread

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

def logged_in(current_user):
    """Returns True if user is logged in. If not, redirects to login page."""
    try:
        _ = current_user.id
        return True
    except Exception:
        return False
    
def get_user_by_id(user_id):
    """Returns user object by id."""
    return app.storage.get_user_by_id(user_id)

def get_user_by_email(email):
    """Returns user object by email."""
    return app.storage.get_user_by_email(email)

def get_booking_by_id(booking_id):
    """Returns booking object by id."""
    return app.storage.get_booking_by_id(booking_id)

def get_booking_by_user_id(user_id):
    """Returns booking object by user id."""
    return app.storage.get_booking_by_user_id(user_id)

def get_destination_by_id(destination_id):
    """Returns destination object by id."""
    return app.storage.get_destination_by_id(destination_id)

def get_flight_by_id(flight_id):
    """Returns flight object by id."""
    return app.storage.get_flight_by_id(flight_id)

def get_hotel_by_id(hotel_id):
    """Returns hotel object by id."""
    return app.storage.get_hotel_by_id(hotel_id)

def get_payment_by_id(payment_id):
    """Returns payment object by id."""
    return app.storage.get_payment_by_id(payment_id)

def get_payment_by_user_id(user_id):
    """Returns payment object by user id."""
    return app.storage.get_payment_by_user_id(user_id)

def get_payment_by_booking_id(booking_id):
    """Returns payment object by booking id."""
    return app.storage.get_payment_by_booking_id(booking_id)

def is_booking_valid(booking):
    """Returns True if booking is valid. If not, returns False."""
    if booking is None:
        return False
    if booking.user_id != current_user.id:
        return False
    if booking.flight_id is None:
        return False
    if booking.hotel_id is None:
        return False
    if booking.destination_id is None:
        return False
    if booking.bus_id is None:
        return False
    booking.payment_id is not None
    return True

def email_confirm_trip(booking):
    """Sends email to user confirming trip."""
    msg = Message('Booking Confirmation', You have successfully booked your trip to {booking.destination.name} from {booking.flight.departure_date} to {booking.flight.return_date}. Your hotel is {booking.hotel.name} and your flight number is {booking.flight.flight_number}. Your total cost is {booking.payment.amount}. Thank you for using our service!)
    msg.add_recipient(current_user.email)
    mail.send(msg)

def email_cancel_trip(booking):
    """Sends email to user cancelling trip."""
    msg = Message('Booking Cancellation', You have successfully cancelled your trip to {booking.destination.name} from {booking.flight.departure_date} to {booking.flight.return_date}. Your hotel is {booking.hotel.name} and your flight number is {booking.flight.flight_number}. Your total cost is {booking.payment.amount}. Thank you for using our service!)
    msg.add_recipient(current_user.email)
    mail.send(msg)

def skip_hotel(destination, booking):
    """Returns True if hotel is not required. If not, returns False."""
    return destination.hotel_id is None

def skip_flight(destination, booking):
    """Returns True if flight is not required. If not, returns False."""
    return destination.flight_id is None

def skip_bus(destination, booking):
    """Returns True if bus is not required. If not, returns False."""
    return destination.bus_id is None
