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
        welcome_Msg = 'Welcome ' + username
        #TODO implement session keys
        return jsonify({'Message': welcome_Msg})
    else:
        password_Incorrect_Msg = 'Incorrect Password'

        return jsonify({'Message': password_Incorrect_Msg})

@app.route('/list_rosters')
def list_rosters():
    rosters = Roster.query.all()
    return render_template('list_rosters.html',rosters=rosters)

@app.route('/list_students')
def list_students():
    students = Student.query.all()
    return render_template('list_students.html', students=students, title='All students:')

@app.route('/single_roster')
def single_roster():
    '''When making the request, be sure to add a roster id in the url in a query string eg: localhost:5000/single_roster?roster_id=1'''
    roster_id = request.args.get('roster_id')
    roster = Roster.query.filter_by(id=roster_id).first()
    student_roster_relationships = Roster_Student_Relationship.query.filter_by(roster_id=roster_id).all()
    students = []


    if not roster:
        errorMSG = 'No roster was found with that id'
        return render_template('single_roster.html',errorMSG=errorMSG)

    if not student_roster_relationships:
        errorMSG = 'No students have been added to this roster'
        return render_template('single_roster.html', roster=roster,errorMSG=errorMSG)

    for relationship in student_roster_relationships:
        student = Student.query.filter_by(id=relationship.student_id).first()
        students.append(student)

    return render_template('single_roster.html',students=students,roster=roster)

@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'GET':
        #TODO: Create add_student.html template and render it here
        return '<h1>This is where the add student form will be rendered</h1>'
    else:
        name = request.form['name']
        notes = request.form['notes']
        new_Student = Student(name, notes)
        db.session.add(new_Student)
        db.session.commit()
        return redirect('/student_profile?student_id='+ str(new_Student.id))

@app.route('/add_roster', methods=['POST','GET'])
def add_roster():
    if request.method == 'GET':
        #TODO: Create add_roster.html
        return '<h1>Here will be a form to add a roster</h1>'
    else:
        course_name = request.form['course_name']
        new_roster = Roster(course_name)
        db.session.add(new_roster)
        db.session.commit()
        return redirect('/single_roster?roster_id=' + str(new_roster.id))

@app.route('/student_profile')
def single_student():
    '''When making the request, be sure to add a roster id in the url in a query string eg: localhost:5000/student_profile?student_id=1'''
    student_Id = request.args.get('student_id')
    student = Student.query.filter_by(id=student_Id).first()
    if not student:
        errorMSG = 'There is no student in the database with that id'
        return render_template('student_profile.html', errorMSG=errorMSG)

    return render_template('student_profile.html', student=student)

@app.route('/add_student_to_roster', methods=['POST'])
def add_student_to_roster():
    student_id = request.form['student_id']
    roster_id = request.form['roster_id']
    new_relationship = Roster_Student_Relationship(roster_id,student_id)
    db.session.add(new_relationship)
    db.session.commit()
    #TODO figure out a way to add more than one student to a roster at a time

    return redirect('/single_roster?roster_id='+str(roster_id))

if __name__ == '__main__':
    app.run()
