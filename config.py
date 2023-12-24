from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from datetime import timedelta

import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.urandom(24)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)
