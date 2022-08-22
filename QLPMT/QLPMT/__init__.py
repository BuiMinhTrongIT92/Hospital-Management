from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
import os


app = Flask(__name__)
app.secret_key = '%*&&*GJVGHHFCHGFYRT^%$^%^*&(&^I&%%*^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0339151784@localhost/qlpmtdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
login = LoginManager(app=app)
db = SQLAlchemy(app = app)


app.config["PAGESIZE"] = 3
cloudinary.config(
    cloud_name= 'dvndzeuhz',
    api_key= '683892731564991',
    api_secret= 'Wjw4Qkw1mOWwRm96P9xU1BS6bKA'
)


