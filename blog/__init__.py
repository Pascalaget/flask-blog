from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


CLOUDSQL_CONNECTION = os.environ.get('CLOUDSQL_CONNECTION')


app.config['SQLALCHEMY_DATABASE_URI'] = CLOUDSQL_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from blog import routes