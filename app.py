from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True #displays runtime errors in terminal
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://attendenceapp:attendenceapp@localhost:8889/attendenceapp'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
