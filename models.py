from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(120))
    rosters = db.relationship('Roster', backref='user')
    students = db.relationship('Student', backref='user')


    def __init__(self,email,password):
        self.email = email
        self.password = password



association_table = db.Table('roster_student',
    db.Column('roster_id', db.Integer, db.ForeignKey('roster.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)


class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80))
    students = db.relationship('Student', secondary=association_table, backref='rosters', order_by="Student.first_name")
    sessions = db.relationship('Session', backref='roster', order_by="Session.name")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,course_name,user_id):
        self.course_name = course_name
        self.user_id = user_id


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    notes = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    attendences = db.relationship('Attendence', backref='student')



    def __init__(self, first_name,last_name, phone, notes, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.notes = notes
        self.user_id = user_id

    def __repr__(self):
        return '<Student %r' % self.name


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roster_id = db.Column(db.Integer, db.ForeignKey('roster.id'))
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    attendences = db.relationship('Attendence', backref='session', cascade="all")

    def __init__(self, name, date, start, end):
        self.name = name
        self.date = date
        self.start = start
        self.end = end


class Attendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    absent = db.Column(db.Boolean, default=False)
    checkin_time = db.Column(db.DateTime)
    checkout_time = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('session_id', 'student_id'),
    )
