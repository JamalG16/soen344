from application.TDG import RoomTDG

def roomExists(roomNumber, clinic_id):
	return RoomTDG.find(roomNumber, clinic_id) is not None

def getRoom(roomNumber, clinic_id):
	return RoomTDG.find(roomNumber=roomNumber, clinic_id=clinic_id)

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

def getAllRoomNumbersByClinic(clinic_id):
	listOfRooms = RoomTDG.findAllAtClinic(clinic_id)
	listOfRoomNumbers = []
	if listOfRooms is None or len(listOfRooms) == 0:
		return []
	else:
		for room in listOfRooms:
			listOfRoomNumbers.append(room.roomNumber)
	return listOfRoomNumbers

# creates room
def createRoom(roomNumber, clinic_id):
	reponse = False
	if roomExists(roomNumber, clinic_id):
		reponse =  False
	else:
		RoomTDG.create(roomNumber, clinic_id)
		reponse = True
	return reponse
