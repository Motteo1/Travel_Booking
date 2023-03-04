#!/usr/bin/python3
"""Module for Flask Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sys
sys.path.append("C:/Users/TIM/Desktop/Code/Travel_Booking/")
from src.classes import storage

# python classes that autoconvert to HTML forms in templates
ENTITY_TYPES = {
    'destination': 'Destination',
    'hotel': 'Hotel',
    'flight': 'Flight',
    'bus': 'Bus',
    'payment': 'Payment',
}

class BookingForm(FlaskForm):
    """Form for creating a booking"""
    # form fields
    fields = {}
    for entity_type, label in ENTITY_TYPES.items():
        fields[entity_type] = SelectField(label, choices=[], validators=[DataRequired()])
    fields['book_button'] = SubmitField('Book')

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for entity_type, field in self.fields.items():
            if entity_type == 'book_button':
                continue
            field.choices = [('', f'Select a {ENTITY_TYPES[entity_type]}')] + [(entity.id, entity.name) for entity in storage.get_all_entities(entity_type)]
            setattr(self, entity_type, field)
        setattr(self, 'book_button', self.fields['book_button'])

class LoginForm(FlaskForm):
    """Form for logging in"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Form for new user registration"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """Check if email is already registered"""
        if user := storage.get_user_by_email(email.data):
            raise ValidationError('That email is already taken. Please choose a different one.')


