from application.models.RoomSchedule import RoomSchedule
from index import db

# return all of a room's timeslots
def findAllbyRoom(roomNumber):
    return RoomSchedule.query.filter_by(roomNumber=roomNumber).timeSlots

# return all of a date's timeslots
def findAllbyDate(date):
    return RoomSchedule.query.filter_by(date=date).all()

def findAllRoomNumbers():
    return RoomSchedule.query.all()

# return all available room numbers b
# return all timeslots based on room number and date
def find(roomNumber, date):
    return RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first().timeSlots
    
# create timeslots of a room on a specific date
def create(roomNumber,timeSlots, date):
    newRoomSchedule = RoomSchedule(roomNumber=roomNumber, timeSlots=timeSlots, date=date)
    db.session.add(newRoomSchedule)
    db.session.commit()

# update a room's timeslots on a specific date
def update(roomNumber, date, timeSlots):
    RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first().timeSlots = timeSlots
    db.session.commit()