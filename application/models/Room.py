from index import db
from datetime import datetime
from .Schedule import createTimeSlots

class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)
	timeSlots = db.Column(db.PickleType, nullable=False)

	def __iter__(self):
		yield 'roomNumber', self.roomNumber
		yield 'timeSlots', self.timeSlots

# Initializes the database
db.create_all()

def roomExists(roomNumber):
	return Room.query.filter_by(roomNumber=roomNumber).first() is not None

def createRoom(roomNumber):
	reponse = False
	if roomExists(roomNumber):
		reponse =  False
	else:
		newRoom = Room(roomNumber=roomNumber, timeSlots=createTimeSlots())
		db.session.add(newRoom)
		db.session.commit()
		reponse = True
	return reponse

# TO DO
def roomAvailable(roomNumber, time):
	return True