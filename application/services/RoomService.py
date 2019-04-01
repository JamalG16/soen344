from application.TDG import RoomTDG

def roomExists(roomNumber, clinic):
	return RoomTDG.find(roomNumber, clinic) is not None

def getRoom(roomNumber, clinic):
	return RoomTDG.find(roomNumber, clinic)

def getAllRooms():
	return RoomTDG.findAll()

def getAllRoomNumbers():
	listOfRooms = RoomTDG.findAll()
	listOfRoomNumbers = []
	if listOfRooms is None or len(listOfRooms) == 0:
		return []
	else:
		for room in listOfRooms:
			listOfRoomNumbers.append(room.roomNumber)
	return listOfRoomNumbers

# creates room
def createRoom(roomNumber, clinic):
	reponse = False
	if roomExists(roomNumber, clinic):
		reponse =  False
	else:
		RoomTDG.create(roomNumber, clinic)
		reponse = True
	return reponse
