from app import db

class Roster(Model.db):
    id = db.Column(db.Integer, primary_key=True)
    course_Name = db.Column(db.String(80))
    students = db.Column(db.Integer, ForeignKey='student.id')

class Student(Model.db):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    notes = db.Column(db.String(250))
    rosters = db.relationship('Roster', backref='student')


    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __repr__(self):
        return '<Student %r' self.name
