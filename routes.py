#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""APP"""
import sys
import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_cors import CORS
import hashlib
import app
from werkzeug.security import generate_password_hash, check_password_hash
from classes.models import User, Booking, Destination, Flight, Hotel
from classes import storage

# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/users', methods=['GET'])
def index():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    count = storage.count()
    for user in storage.all(User).values():
        if user.id == uin:
            return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404

@app.route('/api/v1/users', methods=['POST'])
def create():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['destination'] and data['flight'] and data['hotel']:
                destination = storage.get(Destination, data['destination'])
                flight = storage.get(Flight, data['flight'])
                hotel = storage.get(Hotel, data['hotel'])
                if destination and flight and hotel:
                    booking = Booking()
                    booking.user_id = uin
                    booking.destination_id = destination.id
                    booking.flight_id = flight.id
                    booking.hotel_id = hotel.id
                    storage.new(booking)
                    storage.save()
                    return jsonify(booking.to_dict()), 201
                return jsonify({"error": "Not found"}), 404
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/users/<user_id>', methods=['GET', 'DELETE'])
def get_delete(user_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        user = storage.get(User, user_id)
        if user:
            if request.method == 'GET':
                return jsonify(user.to_dict())
            if request.method == 'DELETE':
                storage.delete(user)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update(user_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        user = storage.get(User, user_id)
        if user:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'email', 'created_at', 'updated_at']:
                        setattr(user, k, v)
                storage.save()
                return jsonify(user.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/destinations', methods=['GET'])
def index_destinations():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        destinations = storage.all(Destination).values()
        return jsonify([destination.to_dict() for destination in destinations])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/destinations', methods=['POST'])
def create_destination():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['name'] and data['description']:
                destination = Destination()
                destination.name = data['name']
                destination.description = data['description']
                storage.new(destination)
                storage.save()
                return jsonify(destination.to_dict()), 201
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/destinations/<destination_id>', methods=['GET', 'DELETE'])
def get_delete_destination(destination_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        destination = storage.get(Destination, destination_id)
        if destination:
            if request.method == 'GET':
                return jsonify(destination.to_dict())
            if request.method == 'DELETE':
                storage.delete(destination)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/destinations/<destination_id>', methods=['PUT'])
def update_destination(destination_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        destination = storage.get(Destination, destination_id)
        if destination:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(destination, k, v)
                storage.save()
                return jsonify(destination.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/flights', methods=['GET'])
def index_flights():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        flights = storage.all(Flight).values()
        return jsonify([flight.to_dict() for flight in flights])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/flights', methods=['POST'])
def create_flight():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['destination'] and data['departure'] and data['arrival']:
                destination = storage.get(Destination, data['destination'])
                if destination:
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
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/flights/<flight_id>', methods=['GET', 'DELETE'])
def get_delete_flight(flight_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        flight = storage.get(Flight, flight_id)
        if flight:
            if request.method == 'GET':
                return jsonify(flight.to_dict())
            if request.method == 'DELETE':
                storage.delete(flight)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/flights/<flight_id>', methods=['PUT'])
def update_flight(flight_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        flight = storage.get(Flight, flight_id)
        if flight:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(flight, k, v)
                storage.save()
                return jsonify(flight.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/hotel', methods=['GET'])
def index_hotels():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        hotels = storage.all(Hotel).values()
        return jsonify([hotel.to_dict() for hotel in hotels])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/hotel', methods=['POST'])
def create_hotel():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['name'] and data['description']:
                hotel = Hotel()
                hotel.name = data['name']
                hotel.description = data['description']
                storage.new(hotel)
                storage.save()
                return jsonify(hotel.to_dict()), 201
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/hotel/<hotel_id>', methods=['GET', 'DELETE'])
def get_delete_hotel(hotel_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        hotel = storage.get(Hotel, hotel_id)
        if hotel:
            if request.method == 'GET':
                return jsonify(hotel.to_dict())
            if request.method == 'DELETE':
                storage.delete(hotel)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/hotel/<hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        hotel = storage.get(Hotel, hotel_id)
        if hotel:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(hotel, k, v)
                storage.save()
                return jsonify(hotel.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/bus', methods=['GET'])
def index_buses():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        buses = storage.all(Bus).values()
        return jsonify([bus.to_dict() for bus in buses])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/bus', methods=['POST'])
def create_bus():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['name'] and data['description']:
                bus = Bus()
                bus.name = data['name']
                bus.description = data['description']
                storage.new(bus)
                storage.save()
                return jsonify(bus.to_dict()), 201
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/bus/<bus_id>', methods=['GET', 'DELETE'])
def get_delete_bus(bus_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        bus = storage.get(Bus, bus_id)
        if bus:
            if request.method == 'GET':
                return jsonify(bus.to_dict())
            if request.method == 'DELETE':
                storage.delete(bus)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/bus/<bus_id>', methods=['PUT'])
def update_bus(bus_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        bus = storage.get(Bus, bus_id)
        if bus:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(bus, k, v)
                storage.save()
                return jsonify(bus.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/payment', methods=['GET'])
def index_payments():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        payments = storage.all(Payment).values()
        return jsonify([payment.to_dict() for payment in payments])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/payment', methods=['POST'])
def create_payment():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['name'] and data['description']:
                payment = Payment()
                payment.name = data['name']
                payment.description = data['description']
                storage.new(payment)
                storage.save()
                return jsonify(payment.to_dict()), 201
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/payment/<payment_id>', methods=['GET', 'DELETE'])
def get_delete_payment(payment_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        payment = storage.get(Payment, payment_id)
        if payment:
            if request.method == 'GET':
                return jsonify(payment.to_dict())
            if request.method == 'DELETE':
                storage.delete(payment)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/payment/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        payment = storage.get(Payment, payment_id)
        if payment:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(payment, k, v)
                storage.save()
                return jsonify(payment.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/api/v1/date', methods=['GET'])
def index_dates():
    """Index"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        dates = storage.all(Date).values()
        return jsonify([date.to_dict() for date in dates])
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/date', methods=['POST'])
def create_date():
    """Create"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        data = request.get_json()
        if data:
            if data['name'] and data['description']:
                date = Date()
                date.name = data['name']
                date.description = data['description']
                storage.new(date)
                storage.save()
                return jsonify(date.to_dict()), 201
            return jsonify({"error": "Missing data"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/date/<date_id>', methods=['GET', 'DELETE'])
def get_delete_date(date_id):
    """Get or delete"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        date = storage.get(Date, date_id)
        if date:
            if request.method == 'GET':
                return jsonify(date.to_dict())
            if request.method == 'DELETE':
                storage.delete(date)
                storage.save()
                return jsonify({}), 200
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/v1/date/<date_id>', methods=['PUT'])
def update_date(date_id):
    """Update"""
    uin = helper_methods.logged_in(current_user)
    if uin:
        date = storage.get(Date, date_id)
        if date:
            data = request.get_json()
            if data:
                for k, v in data.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(date, k, v)
                storage.save()
                return jsonify(date.to_dict()), 200
            return jsonify({"error": "Not a JSON"}), 400
        return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Unauthorized"}), 401

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