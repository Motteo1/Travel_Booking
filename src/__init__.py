from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)


# security against CSRF attacks and cookies modification 
app.config['SECRET_KEY'] = 'ed19db85f910d4624779eda84eb9bc9b15c4a682'


login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Please login to access this page.'

from src import routes