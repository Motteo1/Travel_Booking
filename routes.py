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
    for user in storage.all(User).values():
        if user.id == uin:
            return jsonify(user.to_dict())