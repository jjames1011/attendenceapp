from flask import request, redirect, render_template, session, flash, session
from app import app, db
from models import *
import datetime
import pytz

utc_now = datetime.datetime.now()
pst_now = utc_now.astimezone(pytz.timezone('America/Los_Angeles'))
endpoints_without_login = ['login','signup','static']
@app.before_request
def require_login(): #Control for endpoint access for a non logged in user
    if not ('user_id' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/')
def index():

    return redirect('/list_rosters')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify_pwd = request.form['verify']
        #Check to see if there is already a user in the db with the given email
        duplicate_user = User.query.filter_by(email=email).first()
        if duplicate_user:
            return render_template('signup.html',error_msg='There is already a user with that email')
        if not email or not password or not verify_pwd:
            return render_template('signup.html', error_msg='Please fill out all fields')
        elif password != verify_pwd:
            return render_template('signup.html', error_msg='Passwords did not match')
        else:
            new_User = User(email, password)
            db.session.add(new_User)
            db.session.commit()
            session['user_id'] = new_User.id
            return redirect('/')
    else:
        if 'user_id' in session:
            return redirect('/')
        return render_template('signup.html')
    #TODO Hash passwords


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect('/')
        else:
            return render_template('login.html', error_msg='Wrong username or password')
    else:
        if 'user_id' in session:
            return redirect('/')
        return render_template('login.html')

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/list_rosters')
def list_rosters():
    rosters = Roster.query.filter_by(user_id=session['user_id']).all()
    return render_template('list_rosters.html',rosters=rosters)

@app.route('/list_students')
def list_students():
    students = Student.query.filter_by(user_id=session['user_id']).all()
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
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        notes = request.form['notes']
        phone = request.form['phone']
        error_msg = ''
        #Checks if there is a student in the database with the same first and last names
        duplicate_student = Student.query.filter_by(first_name=first_name,last_name=last_name).first()
        if duplicate_student:
            error_msg = 'Oops It looks like there is already a student with that name.'

        if not first_name or not last_name:
            error_msg = "Please fill out both name fields"

        if not error_msg:
            new_Student = Student(first_name,last_name, phone, notes,session['user_id'])
            db.session.add(new_Student)
            db.session.commit()
            return redirect('/student_profile?student_id='+ str(new_Student.id))
        else:
            return render_template('add_student.html', error_msg=error_msg)

    return render_template('add_student.html')

@app.route('/update_student', methods=['POST','GET'])
def update_student():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        student = Student.query.filter_by(id=student_id).first()
        return render_template('edit_profile.html', title='update student', student=student)
    else:
        student_id = request.args.get('student_id')
        new_notes = request.form['notes']
        new_phone = request.form['phone']
        student = Student.query.filter_by(id=student_id).first()
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
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
        new_roster = Roster(course_name,session['user_id'])
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

        name = "Session " + str(len(roster.sessions) + 1)
        date = datetime.datetime.strptime(request.form['session_date'], '%Y-%m-%d')
        start = datetime.datetime.strptime(request.form['session_start'], '%H:%M')
        end = datetime.datetime.strptime(request.form['session_end'], '%H:%M')
        new_session = Session(name, date, start, end)
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
    title = student.last_name + ', ' + student.first_name
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
        new_students = Student.query.filter(~Student.rosters.contains(roster)).all()

        return render_template('add_student_to_roster.html', students=new_students, roster=roster)


@app.route('/update_attendences', methods=['POST'])
def update_attendences():
    session_id = request.form.get("session_id")
    session = Session.query.filter_by(id=session_id).first()

    if not session:
        return 'Session was not found'

    checkin_list = [int(id) for id in request.form.getlist('checkin')]
    checkout_list = [int(id) for id in request.form.getlist('checkout')]
    absent_list = [int(id) for id in request.form.getlist('absent')]

    for attendence in session.attendences:
        if attendence.id in absent_list:
            attendence.absent = True
            attendence.checkin_time = None
            attendence.checkout_time = None
        else:
            if attendence.id in checkin_list:
                if not attendence.checkin_time:
                    attendence.checkin_time = pst_now
            else:
                attendence.checkin_time = None
                attendence.checkout_time = None

            if attendence.id in checkout_list:
                if not attendence.checkout_time and attendence.checkin_time:
                    attendence.checkout_time = pst_now
            else:
                attendence.checkout_time = None

    db.session.commit()
    return redirect('/single_session?session_id='+str(session_id))


#The secret key should be kept a secret when deployed. Meaning not on github
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()
