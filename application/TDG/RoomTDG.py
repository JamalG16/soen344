from application.models.Room import Room
from index import db

# Returns admin if found
def find(roomNumber, clinic_id):
    return Room.query.filter_by(roomNumber=roomNumber, clinic_id=clinic_id).first()

# find all room numbers
def findAll():
    return db.session.query(Room.roomNumber).all()

def create(roomNumber, clinic_id):
    newRoom = Room(roomNumber=roomNumber, clinic_id=clinic_id)
    db.session.add(newRoom)
    db.session.commit()
