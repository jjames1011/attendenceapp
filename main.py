from flask import request, redirect, render_template, session, flash, jsonify
from app import app, db
from models import Student, Roster, Roster_Student_Relationship

@app.route('/')
def index():
    rosters = Roster.query.all()
    title = 'Rosters:'
    print(rosters)
    output = []
    for roster in rosters:
        roster_data = {}
        roster_data['roster_id'] = roster.id
        roster_data['name'] = roster.course_Name
        output.append(roster_data)
    return jsonify({'rosters' : output})

@app.route('/single_roster')
'''When making the api request, be sure to add a roster id in the url in a query string eg: localhost:5000/single_roster?roster_id=1'''
def single_roster():
    roster_Id = request.args.get('roster_id')
    roster = Roster.query.filter_by(id=roster_Id).first()
    students = Roster_Student_Relationship.query.filter_by(roster_Id=roster_Id).all()

    if not students:
        return jsonify({'Message':'There are no students in the db'})
    output = []
    for student in students:
        student_data = {}
        student_data['student_id'] = student.id
        student_data['student_name'] = student.name
        output.append(student_data)
    return jsonify({'students' : output})


if __name__ == '__main__':
    app.run()
