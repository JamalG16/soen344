from index import db

class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)
	clinic = db.Column(db.Integer, primary_key=True)

	def __iter__(self):
		yield 'roomNumber', self.roomNumber
		yield 'clinic', self.clinic

# Initializes the database
db.create_all()
