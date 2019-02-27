from index import db
from datetime import datetime

# PickleType coverts python object to a string so that it can be stored on the database
class TimeSlot(db.Model):
    available = db.Column(db.Boolean, primary_key=True)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    rooms = db.Column(db.PickleType(mutable=True), nullable=False)
