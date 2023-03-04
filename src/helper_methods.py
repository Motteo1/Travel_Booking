#!/usr/bin/python3
"""
HELPER METHODS
    logged_in:      Returns True if user is logged in. If not, redirects to login page.
    is_booking_valid: Returns True if booking contains either flights, hotels or bus. if at least one is present and payment is made, returns True. If not, returns False. payment is taken from trip_cost.
    email_confirm_trip: Sends email to user confirming trip.
    email_cancel_trip: Sends email to user cancelling trip.
    email_confirm_payment: Sends email to user confirming payment.
    trip_cost: Calculates total cost of trip.

"""
from datetime import date, datetime
from flask import Flask
from flask_mail import Mail, Message
from flask_login import current_user
import os
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
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

def trip_cost(booking):
    """Calculates total cost of trip."""
    cost = 0
    if booking.flight is not None:
        cost += booking.flight.price
    if booking.hotel is not None:
        cost += booking.hotel.price
    if booking.bus is not None:
        cost += booking.bus.price
    return cost

def is_booking_valid(booking):
    """Returns True if booking contains either flights, hotels or bus. if at least one is present and payment is made, returns True. If not, returns False. payment is taken from trip_cost."""
    if booking.flight is None and booking.hotel is None and booking.bus is None:
        return False
    return booking.payment is not None


def email_confirm_trip(booking):
    """Sends email to user confirming trip."""
    msg = Message('Booking Confirmation', body=f"You have Successfully booked your trip to {booking.destination.name} from {booking.flight.departure_date} to {booking.flight.return_date}. Your hotel is {booking.hotel.name} and your flight number is {booking.flight.flight_number}. Your total cost is {booking.payment.amount}. Thank you for using our service!")
    msg.add_recipient(current_user.email)
    mail.send(msg)

def email_confirm_payment(payment):
    """Sends email to user confirming payment."""
    msg = Message('Payment Confirmation', body=f"You have successfully paid ${payment.amount} for your trip to {payment.booking.destination.name} from {payment.booking.flight.departure_date} to {payment.booking.flight.return_date}. Your hotel is {payment.booking.hotel.name} and your flight number is {payment.booking.flight.flight_number}. Thank you for using our service!")
    msg.add_recipient(current_user.email)
    mail.send(msg)

def email_cancel_trip(booking):
    """Sends email to user cancelling trip."""
    msg = Message('Booking Cancellation', body=f"You have successfully cancelled your trip to {booking.destination.name} from {booking.flight.departure_date} to {booking.flight.return_date}. Your hotel is {booking.hotel.name} and your flight number is {booking.flight.flight_number}. Your total cost is {booking.payment.amount}. Thank you for using our service!")
    msg.add_recipient(current_user.email)
    mail.send(msg)


