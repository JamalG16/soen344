from index import db
from datetime import datetime
from datetime import time

# PickleType coverts python object to a string so that it can be stored on the database
class DoctorSchedule(db.Model):
    permit_number = db.Column(db.String(), nullable=False, primary_key=True)
    date = db.Column(db.String(), nullable=False, primary_key=True)
    timeSlots = db.Column(db.String(), nullable=False)

    def __iter__(self):
        yield 'permit_number', self.permit_number
        yield 'date', self.date
        yield 'timeSlots', self.timeSlots

# Initializes the database
db.create_all()