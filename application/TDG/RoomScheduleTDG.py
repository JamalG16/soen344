from application.models.RoomSchedule import RoomSchedule
from index import db

# return all timeslots based on room number and date
def find(date, roomNumber):
    return RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first()
    
# create timeslots of a room on a specific date
def create(roomNumber,timeSlots, date):
    newRoomSchedule = RoomSchedule(roomNumber=roomNumber, timeSlots=timeSlots, date=date)
    db.session.add(newRoomSchedule)
    db.session.commit()

# update a room's timeslots on a specific date
def update(roomNumber, date, newTimeSlots):
    RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first().timeSlots = newTimeSlots
    db.session.commit()