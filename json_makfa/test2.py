class Student(object):
    '''The model, a plain, ol python class'''
    def __init__(self, name, email, enrolled):
        self.name = name
        self.email = email
        self.enrolled = enrolled

    def __repr__(self):
        return "<Student(%r, %r)>" % (self.name, self.email)

    def make_dict(self):
        return {'name': self.name, 'email': self.email}



import sqlalchemy
metadata = sqlalchemy.MetaData()
students_table = sqlalchemy.Table('students', metadata,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('name', sqlalchemy.String(100)),
        sqlalchemy.Column('email', sqlalchemy.String(100)),
        sqlalchemy.Column('enrolled', sqlalchemy.Date)
    )

# connect the database.  substitute the needed values.
engine = sqlalchemy.create_engine('mysql://user:pass@Host/database')

# if needed, create the table:
metadata.create_all(engine)

# map the model to the table
import sqlalchemy.orm
sqlalchemy.orm.mapper(Student, students_table)

# now you can issue queries against the database using the mapping:
non_students = engine.query(Student).filter_by(enrolled=None)

# and lets make some json out of it:
import json
non_students_dicts = ( student.make_dict() for student in non_students)
students_json = json.dumps(non_students_dicts)