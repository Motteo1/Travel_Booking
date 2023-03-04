#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""APP"""
from flask import Flask, request, jsonify, abort, flash, url_for, make_response, session, render_template, redirect
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

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for existing users"""
    form = LoginForm()
    if form.validate_on_submit():
        user = helper_methods.get_user_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """sign-up page for new users"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        storage.save(user)
        flash('Welcome to My Travel!')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    """Home"""
    return render_template('home.html')

@app.route('/book', methods=['GET', 'POST'])
def booking():
    """Post Booking to DB if logged in
    else save booking to session and redirect to login"""
    form = BookingForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            booking = Booking()
            for entity_type, field in form.fields.items():
                if entity_type != 'book_button':
                    setattr(booking, entity_type, storage.get_entity_by_id(entity_type, field.data))
            storage.save(booking)
            return redirect(url_for('home'))
    elif form.validate_on_submit():
        session['booking'] = {entity_type: field.data for entity_type, field in form.fields.items()}
        return redirect(url_for('login'))
    return render_template('book_trip.html', form=form)

@app.errorhandler(404)
def not_found(error):
    """Return custom 404 error
        return render_template('404.html'), 404"""
    return (({'error': 'Not found'}), 404)

@app.after_request
def after_request(response):
    """CORS headers"""
    #allow access from other domains
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
