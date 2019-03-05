from index import db
from datetime import datetime
from .DoctorSchedule import createTimeSlots, format, getTimeSlots, makeAvailable, makeUnavailable, getNextTimeSlot

class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)

	def __iter__(self):
		yield 'roomNumber', self.roomNumber

# Initializes the database
db.create_all()

def roomExists(roomNumber):
	return Room.query.filter_by(roomNumber=roomNumber).first() is not None

def getRoom(roomNumber):
	return Room.query.filter_by(roomNumber=roomNumber).first()

# creates room
def createRoom(roomNumber):
	reponse = False
	if roomExists(roomNumber):
		reponse =  False
	else:
		newRoom = Room(roomNumber=roomNumber)
		createTimeSlots(owner=roomNumber)
		db.session.add(newRoom)
		db.session.commit()
		reponse = True
	return reponse

# get the timeslots of a room
def getRoomTimeSlots(roomNumber):
	if roomExists(roomNumber):
		roomTimeSlots = format(getTimeSlots(roomNumber))
		return roomTimeSlots
	else:
		return False

# check if room is available at a specific time
def roomAvailable(roomNumber, time):
	if roomExists(roomNumber):
		roomTimeSlots = format(getTimeSlots(roomNumber))
		time = time + ':true'
		return time in roomTimeSlots
	else:
		return False

# Returns true if room's timeslot has been modified.
def toggleRoomTimeSlot(roomNumber, time):
	response = False
	room = getRoom(roomNumber)
	if room is not None:
		if roomAvailable(roomNumber, time):
			makeUnavailable(roomNumber, time)
		else:
			makeAvailable(roomNumber, time)
		response = True
	return response

# check if there is an available room at a specific time. If so, return the first room found to be available.
# Else, return None.
def findRoomAtTime(time):
	roomNumber = None
	for room in db.session.query(Room.roomNumber).all():
		if roomAvailable(room.roomNumber, time):
			roomNumber = room.roomNumber
			break
	return roomNumber

# Given a time, get a list that has all rooms available at the specified time.
# Then, check these rooms to find if a room is available for 3 consecutive time slots.
# Return a room, else return None.
def findRoomForAnnual(time):
	roomNumbers = []
	nextTimeSlot = None
	for room in db.session.query(Room.roomNumber).all():
		if roomAvailable(room.roomNumber, time):
			roomNumbers.append(room.roomNumber)
	for roomNumber in roomNumbers:
		nextTimeSlot = getNextTimeSlot(roomNumber, time)
		if nextTimeSlot is not None:
			if roomAvailable(roomNumber, nextTimeSlot):
				nextTimeSlot = getNextTimeSlot(roomNumber, nextTimeSlot)
				if nextTimeSlot is not None:
					if roomAvailable(roomNumber, nextTimeSlot):
						return roomNumber
	return None
	