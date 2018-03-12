from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True #displays runtime errors in terminal
#This next line will differ based on how you config your db on your machine locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://attendenceapp:attendenceapp@localhost:8889/attendenceapp'
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)
