from flask import Flask
from flask_modals import Modal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'topsecretkey'
modal = Modal(app)

from app import routes
