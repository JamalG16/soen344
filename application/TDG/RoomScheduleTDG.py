from application.models.RoomSchedule import RoomSchedule
from index import db

# return all room schedules based on a date
def find(date):
    return RoomSchedule.query.filter_by(date=date).all()

# return all timeslots based on room number and date
def find(date, roomNumber, clinic_id):
    return RoomSchedule.query.filter_by(roomNumber=roomNumber, clinic_id=clinic_id, date=date).first()

# create timeslots of a room on a specific date
def create(roomNumber,clinic_id, timeSlots, date):
    newRoomSchedule = RoomSchedule(roomNumber=roomNumber, clinic_id=clinic_id, timeSlots=timeSlots, date=date)
    db.session.add(newRoomSchedule)
    db.session.commit()

# update a room's timeslots on a specific date
def update(roomNumber, clinic_id, date, newTimeSlots):
    RoomSchedule.query.filter_by(roomNumber=roomNumber, clinic_id=clinic_id, date=date).first().timeSlots = newTimeSlots
    db.session.commit()
