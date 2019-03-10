from application.models.Room import Room
from application.TDG import RoomTDG
from index import db

def roomExists(roomNumber):
	return RoomTDG.find(roomNumber) is not None

def getRoom(roomNumber):
	return RoomTDG.find(roomNumber)

def getAllRooms():
	return RoomTDG.findAll()

# creates room
def createRoom(roomNumber):
	reponse = False
	if roomExists(roomNumber):
		reponse =  False
	else:
		RoomTDG.create(roomNumber)
		reponse = True
	return reponse