from application.models.Room import Room
from index import db

# Returns admin if found
def find(roomNumber):
    return Room.query.filter_by(roomNumber=roomNumber, clinic=clinic).first()

# find all room numbers
def findAll():
    return db.session.query(Room.roomNumber).all()

def create(roomNumber):
    newRoom = Room(roomNumber=roomNumber, clinic=clinic)
    db.session.add(newRoom)
    db.session.commit()
