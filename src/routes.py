#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""APP"""
from flask import request, jsonify, abort, flash, url_for, make_response, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_cors import CORS
from flask_mail import Mail, Message
import hashlib
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src import app
from src.classes.models import User, Booking, Destination, Flight, Hotel, Payment, Bus, Date
from src.forms import LoginForm, RegistrationForm, BookingForm
from src.classes import storage
from src import helper_methods
import random
import string
from werkzeug.security import check_password_hash



# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/users', methods=['GET'])
def index_user():
    """Search for user"""
    uin = helper_methods.logged_in(current_user)
    count = storage.count()
    for user in storage.all(User).values():
        if user.id == uin:
            return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users', methods=['POST'])
def create():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['destination'] and data['flight'] and data['hotel'] and data['bus'] and data['payment'] and data['date']:
            destination = storage.get(Destination, data['destination'])
            flight = storage.get(Flight, data['flight'])
            hotel = storage.get(Hotel, data['hotel'])
            bus = storage.get(Bus, data['bus'])
            payment = storage.get(Payment, data['payment'])
            if destination and flight and hotel and bus and payment:
                booking = Booking()
                booking.user_id = uin
                booking.destination_id = destination.id
                booking.flight_id = flight.id
                booking.hotel_id = hotel.id
                booking.bus_id = bus.id
                booking.payment_id = payment.id
                booking.date_id = data['date']
                booking.total = destination.price + flight.price + hotel.price + bus.price
                storage.new(booking)
                storage.save()
                return jsonify(booking.to_dict()), 201
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/users/<user_id>', methods=['GET', 'DELETE'])
def get_delete(user_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if request.method == 'GET':
            return jsonify(user.to_dict())
        if request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update(user_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(user, k, v)
            storage.save()
            return jsonify(user.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings', methods=['GET'])
def get_bookings(user_id):
    """Get bookings"""
    if uin := helper_methods.logged_in(current_user):
        if user := storage.get(User, user_id):
            bookings = storage.all(Booking).values()
            return jsonify([booking.to_dict() for booking in bookings if booking.user_id == user.id])
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>', methods=['GET', 'DELETE'])
def get_delete_booking(user_id, booking_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if request.method == 'GET':
                return jsonify(booking.to_dict())
            if request.method == 'DELETE':
                storage.delete(booking)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>', methods=['PUT'])
def update_booking(user_id, booking_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if data := request.get_json():
                for k, v in data.items():
                    if k not in ['id', 'user_id', 'destination_id', 'flight_id', 'hotel_id', 'bus_id', 'payment_id', 'date_id', 'created_at', 'updated_at']:
                        setattr(booking, k, v)
                storage.save()
                return jsonify(booking.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/payment', methods=['POST'])
def create_payment(user_id, booking_id):
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if data := request.get_json():
                if data['name'] and data['number'] and data['expiration_date'] and data['cvv']:
                    payment = Payment()
                    payment.name = data['name']
                    payment.number = data['number']
                    payment.expiration_date = data['expiration_date']
                    payment.cvv = data['cvv']
                    payment.booking_id = booking.id
                    storage.new(payment)
                    storage.save()
                    return jsonify(payment.to_dict()), 201
                return jsonify({"error": "Missing data"}), 400
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/payment', methods=['GET', 'DELETE'])
def get_delete_payment(user_id, booking_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if payment := storage.get(Payment, booking.payment_id):
                if request.method == 'GET':
                    return jsonify(payment.to_dict())
                if request.method == 'DELETE':
                    storage.delete(payment)
                    storage.save()
                    return jsonify({}), 200
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/payment', methods=['PUT'])
def update_payment(user_id, booking_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if payment := storage.get(Payment, booking.payment_id):
                if data := request.get_json():
                    for k, v in data.items():
                        if k not in ['id', 'name', 'number', 'expiration_date', 'cvv', 'booking_id', 'created_at', 'updated_at']:
                            setattr(payment, k, v)
                    storage.save()
                    return jsonify(payment.to_dict()), 200
                return jsonify({"error": "Not a JSON"}), 400
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/date', methods=['POST'])
def create_date(user_id, booking_id):
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if data := request.get_json():
                if data['start_date'] and data['end_date']:
                    date = Date()
                    date.start_date = data['start_date']
                    date.end_date = data['end_date']
                    date.booking_id = booking.id
                    storage.new(date)
                    storage.save()
                    return jsonify(date.to_dict()), 201
                return jsonify({"error": "Missing data"}), 400
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/date', methods=['GET', 'DELETE'])
def get_delete_date(user_id, booking_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if date := storage.get(Date, booking.date_id):
                if request.method == 'GET':
                    return jsonify(date.to_dict())
                if request.method == 'DELETE':
                    storage.delete(date)
                    storage.save()
                    return jsonify({}), 200
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/date', methods=['PUT'])
def update_date(user_id, booking_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if date := storage.get(Date, booking.date_id):
                if data := request.get_json():
                    for k, v in data.items():
                        if k not in ['id', 'start_date', 'end_date', 'booking_id', 'created_at', 'updated_at']:
                            setattr(date, k, v)
                    storage.save()
                    return jsonify(date.to_dict()), 200
                return jsonify({"error": "Not a JSON"}), 400
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/destination', methods=['POST'])
def create_destination(user_id, booking_id):
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if data := request.get_json():
                if data['name'] and data['description']:
                    destination = Destination()
                    destination.name = data['name']
                    destination.description = data['description']
                    destination.booking_id = booking.id
                    storage.new(destination)
                    storage.save()
                    return jsonify(destination.to_dict()), 201
                return jsonify({"error": "Missing data"}), 400
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/destination', methods=['GET', 'DELETE'])
def get_delete_destination(user_id, booking_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if destination := storage.get(Destination, booking.destination_id):
                if request.method == 'GET':
                    return jsonify(destination.to_dict())
                if request.method == 'DELETE':
                    storage.delete(destination)
                    storage.save()
                    return jsonify({}), 200
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users/<user_id>/bookings/<booking_id>/destination', methods=['PUT'])
def update_destination(user_id, booking_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if user := storage.get(User, user_id):
        if booking := storage.get(Booking, booking_id):
            if destination := storage.get(Destination, booking.destination_id):
                if data := request.get_json():
                    for k, v in data.items():
                        if k not in ['id', 'name', 'description', 'booking_id', 'created_at', 'updated_at']:
                            setattr(destination, k, v)
                    storage.save()
                    return jsonify(destination.to_dict()), 200
                return jsonify({"error": "Not a JSON"}), 400
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404


@app.route('/api/v1/destinations', methods=['GET'])
def index_destinations():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        destinations = storage.all(Destination).values()
        return jsonify([destination.to_dict() for destination in destinations])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/destinations', methods=['POST'])
def create_new_destination():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['name'] and data['description']:
            destination = Destination()
            destination.name = data['name']
            destination.description = data['description']
            storage.new(destination)
            storage.save()
            return jsonify(destination.to_dict()), 201
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/destinations/<destination_id>', methods=['GET', 'DELETE'])
def get_or_delete_destination(destination_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if destination := storage.get(Destination, destination_id):
        if request.method == 'GET':
            return jsonify(destination.to_dict())
        if request.method == 'DELETE':
            storage.delete(destination)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/destinations/<destination_id>', methods=['PUT'])
def updated_destination(destination_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if destination := storage.get(Destination, destination_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(destination, k, v)
            storage.save()
            return jsonify(destination.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/flights', methods=['GET'])
def index_flights():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        flights = storage.all(Flight).values()
        return jsonify([flight.to_dict() for flight in flights])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/flights', methods=['POST'])
def create_flight():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['destination'] and data['departure'] and data['arrival']:
            if destination := storage.get(Destination, data['destination']):
                flight = Flight()
                flight.destination_id = destination.id
                flight.departure = data['departure']
                flight.arrival = data['arrival']
                storage.new(flight)
                storage.save()
                return jsonify(flight.to_dict()), 201
            return jsonify({"error": "Not found"}), 404
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/flights/<flight_id>', methods=['GET', 'DELETE'])
def get_delete_flight(flight_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if flight := storage.get(Flight, flight_id):
        if request.method == 'GET':
            return jsonify(flight.to_dict())
        if request.method == 'DELETE':
            storage.delete(flight)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/flights/<flight_id>', methods=['PUT'])
def update_flight(flight_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if flight := storage.get(Flight, flight_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(flight, k, v)
            storage.save()
            return jsonify(flight.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app.route('/api/v1/hotel', methods=['GET'])
def index_hotels():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        hotels = storage.all(Hotel).values()
        return jsonify([hotel.to_dict() for hotel in hotels])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/hotel', methods=['POST'])
def create_hotel():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['name'] and data['description']:
            hotel = Hotel()
            hotel.name = data['name']
            hotel.description = data['description']
            storage.new(hotel)
            storage.save()
            return jsonify(hotel.to_dict()), 201
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/hotel/<hotel_id>', methods=['GET', 'DELETE'])
def get_delete_hotel(hotel_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if hotel := storage.get(Hotel, hotel_id):
        if request.method == 'GET':
            return jsonify(hotel.to_dict())
        if request.method == 'DELETE':
            storage.delete(hotel)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/hotel/<hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if hotel := storage.get(Hotel, hotel_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(hotel, k, v)
            storage.save()
            return jsonify(hotel.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/bus', methods=['GET'])
def index_buses():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        buses = storage.all(Bus).values()
        return jsonify([bus.to_dict() for bus in buses])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/bus', methods=['POST'])
def create_bus():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['name'] and data['description']:
            bus = Bus()
            bus.name = data['name']
            bus.description = data['description']
            storage.new(bus)
            storage.save()
            return jsonify(bus.to_dict()), 201
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/bus/<bus_id>', methods=['GET', 'DELETE'])
def get_delete_bus(bus_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if bus := storage.get(Bus, bus_id):
        if request.method == 'GET':
            return jsonify(bus.to_dict())
        if request.method == 'DELETE':
            storage.delete(bus)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/bus/<bus_id>', methods=['PUT'])
def update_bus(bus_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if bus := storage.get(Bus, bus_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(bus, k, v)
            storage.save()
            return jsonify(bus.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app.route('/api/v1/payment', methods=['GET'])
def index_payments():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        payments = storage.all(Payment).values()
        return jsonify([payment.to_dict() for payment in payments])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/payment', methods=['POST'])
def create_new_payment():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['name'] and data['description']:
            payment = Payment()
            payment.name = data['name']
            payment.description = data['description']
            storage.new(payment)
            storage.save()
            return jsonify(payment.to_dict()), 201
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/payment/<payment_id>', methods=['GET', 'DELETE'])
def get_or_delete_payment(payment_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if payment := storage.get(Payment, payment_id):
        if request.method == 'GET':
            return jsonify(payment.to_dict())
        if request.method == 'DELETE':
            storage.delete(payment)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/payment/<payment_id>', methods=['PUT'])
def updated_payment(payment_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if payment := storage.get(Payment, payment_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(payment, k, v)
            storage.save()
            return jsonify(payment.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/date', methods=['GET'])
def index_dates():
    """Index"""
    if uin := helper_methods.logged_in(current_user):
        dates = storage.all(Date).values()
        return jsonify([date.to_dict() for date in dates])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/date', methods=['POST'])
def create_new_date():
    """Create"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if data := request.get_json():
        if data['name'] and data['description']:
            date = Date()
            date.name = data['name']
            date.description = data['description']
            storage.new(date)
            storage.save()
            return jsonify(date.to_dict()), 201
        return jsonify({"error": "Missing data"}), 400
    return jsonify({"error": "Not a JSON"}), 400

@app.route('/api/v1/date/<date_id>', methods=['GET', 'DELETE'])
def get_or_delete_date(date_id):
    """Get or delete"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if date := storage.get(Date, date_id):
        if request.method == 'GET':
            return jsonify(date.to_dict())
        if request.method == 'DELETE':
            storage.delete(date)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/date/<date_id>', methods=['PUT'])
def updated_date(date_id):
    """Update"""
    if not (uin := helper_methods.logged_in(current_user)):
        return jsonify({"error": "Unauthorized"}), 401
    if date := storage.get(Date, date_id):
        if data := request.get_json():
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(date, k, v)
            storage.save()
            return jsonify(date.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(404)
def page_not_found(e):
    """404"""
    return jsonify({"error": "Not found"}), 404


@app.after_request
def after_request(response):
    """CORS"""
    # allow access from other domains
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)