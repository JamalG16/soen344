from index import db

class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)
	available = db.Column(db.Boolean, primary_key=True)

def roomExists(roomNumber):
	return Room.query.filter_by(roomNumber=roomNumber).first() is not None

def createRoom(roomNumber, available):
	reponse = False
	if roomExists(hcnumber):
		reponse =  False
	else:
		newRoom = Room(roomNumber=roomNumber, available=available)
		db.session.add(newRoom)
		db.session.commit()
		reponse = True
	return reponse
