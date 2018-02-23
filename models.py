from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    #Parent,Instructor, Moderator, or Admin
    rank = db.Column(db.String(50))

    def __init__(self,username,password,rank):
        self.username = username
        self.password = password
        self.rank = rank


association_table = db.Table('roster_student',
    db.Column('roster_id', db.Integer, db.ForeignKey('roster.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)


class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80))
    students = db.relationship('Student', secondary=association_table, backref='rosters')
    sessions = db.relationship('Session', backref='roster')

    def __init__(self,course_name):
        self.course_name = course_name


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    notes = db.Column(db.String(250))
    attendences = db.relationship('Attendence', backref='student')

    def __init__(self, name, phone, notes):
        self.name = name
        self.phone = phone
        self.notes = notes

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
    checkin_time = db.Column(db.DateTime)
    checkout_time = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint('session_id', 'student_id'),
    )
