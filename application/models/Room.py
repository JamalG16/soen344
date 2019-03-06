from index import db
from datetime import datetime

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

def getAllRooms():
	return db.session.query(Room.roomNumber).all()

# creates room
def createRoom(roomNumber, date):
	reponse = False
	if roomExists(roomNumber):
		reponse =  False
	else:
		newRoom = Room(roomNumber=roomNumber)
		db.session.add(newRoom)
		db.session.commit()
		reponse = True
	return reponse
