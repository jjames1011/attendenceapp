from app import db

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_Name = db.Column(db.String(80))
    students = db.relationship('Roster_Student_Relationship', backref='roster')


    def __init__(self,course_Name):
        self.course_Name = course_Name

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
    roster_Id = db.Column(db.Integer, db.ForeignKey('roster.id'))
    student_Id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, roster_Id, player_id):
        self.roster_Id = roster_Id
        self.player_id = player_Id
