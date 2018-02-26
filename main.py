from flask import request, redirect, render_template, session, flash, jsonify
from app import app, db
from models import *
import datetime

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

    if not roster:
        errorMSG = 'No roster was found with that id'
        return render_template('single_roster.html',errorMSG=errorMSG)

    if not roster.students:
        errorMSG = 'No students have been added to this roster'
        return render_template('single_roster.html', roster=roster,errorMSG=errorMSG)

    return render_template('single_roster.html', roster=roster)

@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        notes = request.form['notes']
        phone = request.form['phone']

        name_error = ''

        if not name:
            name_error = "Please enter a student's name."

        if not name_error:
            new_Student = Student(name, phone, notes)
            db.session.add(new_Student)
            db.session.commit()
            return redirect('/student_profile?student_id='+ str(new_Student.id))
        else:
            return render_template('add_student.html', name_error=name_error)

    return render_template('add_student.html')

@app.route('/update_student', methods=['POST','GET'])
def update_student():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        return render_template('edit_profile.html', title='update student', student=student)
    else:
        student_id = request.args.get('student_id')
        new_name = request.form['name']
        new_notes = request.form['notes']
        new_phone = request.form['phone']
        student = Student.query.filter_by(id=student_id).first()
        student.name = new_name
        student.notes = new_notes
        student.phone = new_phone
        db.session.commit()
        return redirect('/student_profile?student_id=' + str(student_id))


@app.route('/add_roster', methods=['POST','GET'])
def add_roster():
    if request.method == 'GET':
        return render_template('add_roster.html', title='add roster')
    else:
        course_name = request.form['course_name']
        new_roster = Roster(course_name)
        db.session.add(new_roster)
        db.session.commit()
        return redirect('/single_roster?roster_id=' + str(new_roster.id))


@app.route('/add_session', methods=['POST','GET'])
def add_session():
    no_roster_message = 'No roster associated with this id'

    if request.method == 'GET':
        roster_id = request.args.get('roster_id')
        if not roster_id:
            return 'Roster id required'

        roster = Roster.query.filter_by(id=roster_id).first()
        if not roster:
            return no_roster_message

        return render_template('add_session.html', roster=roster)
    else:
        roster_id = request.form['roster_id']
        roster = Roster.query.filter_by(id=roster_id).first()
        if not roster:
            return no_roster_message

        name = request.form['session_name']
        new_session = Session(name, None, None)
        roster.sessions.append(new_session)
        db.session.flush()

        for student in roster.students:
            attendence = Attendence()
            attendence.student = student
            attendence.session = new_session
            db.session.add(attendence)

        db.session.commit()
        return redirect('/single_roster?roster_id=' + str(roster_id))


@app.route('/single_session')
def single_session():
    session_id = request.args.get('session_id')
    session = Session.query.filter_by(id=session_id).first()

    if not session:
        return 'No session associated with this id'

    return render_template('single_session.html', session=session)


@app.route('/student_profile')
def single_student():
    '''When making the request, be sure to add a roster id in the url in a query string eg: localhost:5000/student_profile?student_id=1'''
    student_Id = request.args.get('student_id')
    student = Student.query.filter_by(id=student_Id).first()
    if not student:
        errorMSG = 'There is no student in the database with that id'
        return render_template('student_profile.html', errorMSG=errorMSG, title='Student not found')
    title = student.name
    return render_template('student_profile.html', student=student, title=title)

@app.route('/add_student_to_roster', methods=['POST', 'GET'])
def add_student_to_roster():
    roster_id = request.args.get('roster_id')
    roster = Roster.query.filter_by(id=roster_id).first()

    if request.method == 'POST':
        student_ids = request.form.getlist('student_id')
        students = Student.query.filter(Student.id.in_(student_ids)).all()

        roster.students.extend(students)
        db.session.commit()

        return redirect('/single_roster?roster_id='+str(roster_id))

    else:
        # gets all students who are not already in this class roster
        new_students = Student.query.filter(~Student.rosters.contains(roster))

        return render_template('add_student_to_roster.html', students=new_students, roster=roster)


@app.route('/update_attendences', methods=['POST'])
def update_attendences():
    session_id = request.form.get("session_id")
    session = Session.query.filter_by(id=session_id).first()

    if not session:
        return 'Session was not found'

    checkin_list = [int(id) for id in request.form.getlist('checkin')]
    checkout_list = [int(id) for id in request.form.getlist('checkout')]

    for attendence in session.attendences:
        if attendence.id in checkin_list:
            if not attendence.checkin_time:
                attendence.checkin_time = datetime.datetime.now(datetime.timezone.utc)
        else:
            attendence.checkin_time = None

        if attendence.id in checkout_list:
            if not attendence.checkout_time:
                attendence.checkout_time = datetime.datetime.now(datetime.timezone.utc)
        else:
            attendence.checkout_time = None

    db.session.commit()

    return redirect('/single_session?session_id='+str(session_id))

if __name__ == '__main__':
    app.run()
