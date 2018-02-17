from app import app, db
from models import *


with app.app_context():
    db.drop_all()
    db.create_all()

    # Start to create default data

    roster1 = Roster('Course 1')
    roster2 = Roster('Course 2')

    db.session.add(roster1)
    db.session.add(roster2)

    student1 = Student('Mary', '555-555-5555', 'This is a note')
    student2 = Student('Cody', '555-555-5555', 'This is a note')
    student3 = Student('Wendy', '555-555-5555', 'This is a note')
    student4 = Student('Olivia', '555-555-5555', 'This is a note')

    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)

    # For getting student and roster id without committing
    db.session.flush()

    roster_student_1 = Roster_Student_Relationship(roster1.id, student1.id)
    roster_student_2 = Roster_Student_Relationship(roster1.id, student2.id)
    roster_student_3 = Roster_Student_Relationship(roster1.id, student3.id)
    roster_student_4 = Roster_Student_Relationship(roster1.id, student4.id)

    db.session.add(roster_student_1)
    db.session.add(roster_student_2)
    db.session.add(roster_student_3)
    db.session.add(roster_student_4)

    db.session.commit()
