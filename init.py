from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)
from app import app, db
from models import *


def drop_all(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


with app.app_context():
    drop_all(db)    
    db.create_all()

    # Start to create default data

    user = User('user@email.com', 123456)
    db.session.add(user)
    db.session.flush()

    roster1 = Roster('Course 1', user.id)
    roster2 = Roster('Course 2', user.id)

    db.session.add(roster1, user.id)
    db.session.add(roster2, user.id)

    student1 = Student('Mary', 'Mary', '555-555-5555', 'This is a note', user.id)
    student2 = Student('Cody', 'Cody', '555-555-5555', 'This is a note', user.id)
    student3 = Student('Wendy', 'Wendy', '555-555-5555', 'This is a note', user.id)
    student4 = Student('Olivia', 'Olivia', '555-555-5555', 'This is a note', user.id)

    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)
    db.session.add(student4)

    # For getting student and roster id without committing
    db.session.flush()

    roster1.students.append(student1)
    roster1.students.append(student2)
    roster1.students.append(student3)
    roster1.students.append(student4)

    db.session.commit()
