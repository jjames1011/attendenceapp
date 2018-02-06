from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Student, Roster, Roster_Student_Relationship

@app.route('/')
def index():
    rosters = Roster.query.all()
    title = 'Rosters:'
    return render_template('list_rosters.html', rosters=rosters, title=title)

if __name__ == '__main__':
    app.run()
