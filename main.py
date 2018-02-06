from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Student, Roster, Roster_Student_Relationship

@app.route('/')
def index():
    rosters = Roster.query.all()
    title = 'Rosters:'
    return render_template('list_rosters.html', rosters=rosters, title=title)

@app.route('/single_roster')
def single_roster():
    roster_Id = request.args.get('roster_id')
    roster = Roster.query.filter_by(id=roster_Id).first()
    students = Roster_Student_Relationship.query.filter_by(roster_Id=roster_Id).all()
    return render_template('single_roster.html', students=students,title=roster.course_Name)


if __name__ == '__main__':
    app.run()
