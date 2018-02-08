from flask import request, redirect, render_template, session, flash, jsonify
from app import app, db
from models import Student, Roster, Roster_Student_Relationship, User

@app.route('/')
def index():
    return redirect('/list_rosters')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    rank = request.form['rank']
    new_User = User(username, password, rank)
    db.session.add(new_User)
    db.session.commit()
    #TODO implement Session key to keep track of logged in username
    #TODO add verification
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'Login Error:','There is no user with that username'})
    elif user.password == password:
        welcome_Msg = 'Welcome '+ username
        #TODO implement session keys
        return jsonify({'Message': welcome_Msg})
    else:
        password_Incorrect_Msg = 'Incorrect Password'
        return jsonify({'Message': password_Incorrect_Msg})



@app.route('/list_rosters')
def list_rosters():
    rosters = Roster.query.all()
    title = 'Rosters:'
    output = []
    for roster in rosters:
        roster_data = {}
        roster_data['roster_id'] = roster.id
        roster_data['name'] = roster.course_Name
        output.append(roster_data)
    return jsonify({'rosters' : output})


@app.route('/single_roster')
def single_roster():
    '''When making the api request, be sure to add a roster id in the url in a query string eg: localhost:5000/single_roster?roster_id=1'''
    roster_Id = request.args.get('roster_id')
    roster = Roster.query.filter_by(id=roster_Id).first()
    students = Roster_Student_Relationship.query.filter_by(roster_Id=roster_Id).all()

    if not students:
        return jsonify({'Message':'There are no students in the database'})
    output = []
    for student in students:
        student_data = {}
        student_data['student_id'] = student.id
        student_data['student_name'] = student.name
        output.append(student_data)
    return jsonify({'students' : output})

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    notes = request.form['notes']
    new_Student = Student(name, notes)
    db.session.add(new_Student)
    db.session.commit()
    return redirect('/student_profile?student_id='+ str(new_Student.id))

@app.route('/add_roster', methods=['POST'])
def add_roster():
    course_Name = request.form['course_Name']
    new_roster = Roster(course_Name)
    db.session.add(new_roster)
    db.session.commit()

    return redirect('/single_roster?roster_id=' + str(new_roster.id))



@app.route('/student_profile')
def single_student():
    '''When making the api request, be sure to add a roster id in the url in a query string eg: localhost:5000/student_profile?student_id=1'''
    student_Id = request.args.get('student_id')
    student = Student.query.filter_by(id=student_Id).first()
    if not student:
        return jsonify({'Message': 'There is no student with that ID in the database'})
    output = []
    student_data = {}
    student_data['student_id'] = student.id
    student_data['student_name'] = student.name
    student_data['student_notes'] = student.notes
    output.append(student_data)

    return jsonify({'Student': output})


if __name__ == '__main__':
    app.run()
