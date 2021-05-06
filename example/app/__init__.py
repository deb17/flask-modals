from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin
from flask_modals import Modal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
modal = Modal(app)


class User(UserMixin):
    def __init__(self, username, password):
        self.id = 1
        self.username = username
        self.password = password


user = User('test', 'pass')


@login.user_loader
def user_loader(id):

    return user


from app import routes
