from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Student, Roster, Roster_Student_Relationship

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
