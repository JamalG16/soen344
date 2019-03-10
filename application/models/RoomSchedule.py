from index import db
from datetime import datetime
from datetime import time
import json

# PickleType coverts python object to a string so that it can be stored on the database
class RoomSchedule(db.Model):
    roomNumber = db.Column(db.String(), nullable=False, primary_key=True)
    date = db.Column(db.String(), nullable=False, primary_key=True)
    timeSlots = db.Column(db.String(), nullable=False)

    def __iter__(self):
        yield 'roomNumber', self.roomNumber
        yield 'timeSlots', self.timeSlots
        yield 'date', self.date

# Initializes the database
db.create_all()

#SLOTS = {time(8,00,00): False,time(8,20,00): False,time(8,40,00): False,time(9,0,00): False,time(9,20,00): False,time(9,40,00): False,time(10,00,00): False,time(10,20,00): False,time(10,40,00): False,time(11,00,00): False,time(11,20,00): False,time(11,40,00): False,time(12,00,00): False,time(12,20,00): False,time(12,40,00): False,time(13,00,00): False,time(13,20,00): False,time(13,40,00): False,time(14,00,00): False,time(14,20,00): False,time(14,40,00): False,time(15,00,00): False,time(15,20,00): False,time(15,40,00): False,time(16,00,00): False,time(16,20,00): False,time(16,40,00): False,time(17,00,00): False,time(17,20,00): False,time(17,40,00): False,time(18,00,00): False,time(18,20,00): False,time(18,40,00): False,time(19,00,00): False,time(19,20,00): False,time(19,40,00): False}
#SLOTS = ['8:00:00','8:20:00','8:40:00','9:00:00','9:20:00','9:40:00','10:00:00','10:20:00','10:40:00','11:00:00','11:20:00','11:40:00','12:00:00','12:20:00','12:40:00','13:00:00','13:20:00','13:40:00','14:00:00','14:20:00','14:40:00','15:00:00','15:20:00','15:40:00','16:00:00','16:20:00','16:40:00','17:00:00','17:20:00','17:40:00','18:00:00','18:20:00','18:40:00','19:00:00','19:20:00','19:40:00']

# Create an with all possible timeslots and whether it is available or not
SLOTS = '8:00:true,8:20:true,8:40:true,9:00:true,9:20:true,9:40:true,10:00:true,10:20:true,10:40:true,11:00:true,11:20:true,11:40:true,12:00:true,12:20:true,12:40:true,13:00:true,13:20:true,13:40:true,14:00:true,14:20:true,14:40:true,15:00:true,15:20:true,15:40:true,16:00:true,16:20:true,16:40:true,17:00:true,17:20:true,17:40:true,18:00:true,18:20:true,18:40:true,19:00:true,19:20:true,19:40:true'

def createTimeSlots(roomNumber, date):
    newRoomSchedule = RoomSchedule(roomNumber=roomNumber, timeSlots=SLOTS, date=date)
    db.session.add(newRoomSchedule)
    db.session.commit()
    return newRoomSchedule

def getAllTimeSlotsByRoom(roomNumber):
    return format(RoomSchedule.query.filter_by(roomNumber=roomNumber).timeSlots)

def getAllTimeSlotsByDate(date):
    return format(RoomSchedule.query.filter_by(date=date).timeSlots)

def getAllRoomsByDate(date):
    if RoomSchedule.query.filter_by(date=date).first() is None:
        return None
    else:
        return format(RoomSchedule.query.filter_by(date=date).first().roomNumber)

def getAllRoomNumbers():
    listOfRooms = RoomSchedule.query.all()
    listOfRoomNumbers=[]
    if listOfRooms is None or len(listOfRooms)==0:
        return []
    else:
        for room in listOfRooms:
            listOfRoomNumbers.append(room.roomNumber)
    return listOfRoomNumbers

def getTimeSlotsByDateAndRoom(roomNumber, date):
    if RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first() is None:
        return None
    else:
        return format(RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first().timeSlots)

# transform timeslots string into an array
def format(timeslots):
	return timeslots.split(",")

# Return true if slot is available, else return false.
def isTimeSlotAvailable(roomNumber, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber, date)
    fulltime = time + ':true'
    return fulltime in timeSlots

# Return the next time slot. If no next time slot, then return None.
def getNextTimeSlot(roomNumber, date, time):
    if time is '19:40':
        return None
    else:
        timeSlots = format(getAllTimeSlotsByRoom(roomNumber))
        index = None
        if isTimeSlotAvailable(roomNumber, date, time):
            index = timeSlots.index(time + ':true')
            return timeSlots[index+1][:-5] #increment the index to get next time slot
        else:
            index = timeSlots.index(time + ':false')
            return timeSlots[index+1][:-6] #increment the index to get next time slot

# makes a timeslot available
def makeTimeSlotAvailable(roomNumber, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber, date)
    index = timeSlots.index(time + ':false')
    timeSlots[index] = time + ':true'
    RoomSchedule.query.filter_by(roomNumber=roomNumber,date=date).first().timeSlots = ','.join(timeSlots) # put back into db as a string
    db.session.commit()

# if the appointment is an annual, make all slots available
def makeTimeSlotAvailableAnnual(roomNumber, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber, date, time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber, date, roomNextTimeSlot)

    makeTimeSlotAvailable(roomNumber, date, time)
    makeTimeSlotAvailable(roomNumber, date, roomNextTimeSlot)
    makeTimeSlotAvailable(roomNumber, date, roomNextNextTimeSlot)
    db.session.commit()

#makes a timeslot unavailable
def makeTimeSlotUnavailable(roomNumber, date, time):
    timeSlots = format(getTimeSlotsByDateAndRoom(roomNumber, date))
    index = timeSlots.index(time + ':true')
    timeSlots[index] = time + ':false'
    RoomSchedule.query.filter_by(roomNumber=roomNumber, date=date).first().timeSlots = ','.join(timeSlots) #put back into db as a string
    db.session.commit()

# if the appointment is an annual, make all slots unavailable
def makeTimeSlotUnavailableAnnual(roomNumber, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber, date, time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber, date, roomNextTimeSlot)

    makeTimeSlotUnavailable(roomNumber, date, time)
    makeTimeSlotUnavailable(roomNumber, date, roomNextTimeSlot)
    makeTimeSlotUnavailable(roomNumber, date, roomNextNextTimeSlot)
    db.session.commit()
