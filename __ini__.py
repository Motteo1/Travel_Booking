from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

# security against CSRF attacks
app.config['SECRET_KEY'] = 'secret'

login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Please login to access this page.'
