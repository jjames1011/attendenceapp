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


class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80))
    students = db.relationship('Roster_Student_Relationship', backref='roster')

    def __init__(self,course_name):
        self.course_name = course_name

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    notes = db.Column(db.String(250))
    rosters = db.relationship('Roster_Student_Relationship', backref='student')


    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __repr__(self):
        return '<Student %r' % self.name

class Roster_Student_Relationship(db.Model):
    '''This is a table to represent the many-to-many relationship between a roster and a student. '''
    id = db.Column(db.Integer, primary_key=True)
    roster_id = db.Column(db.Integer, db.ForeignKey('roster.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, roster_id, student_id):
        self.roster_id = roster_id
        self.student_id = student_id
