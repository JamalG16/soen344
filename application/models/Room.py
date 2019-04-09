from index import db


class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)
	clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), primary_key=True)

	def __iter__(self):
		yield 'roomNumber', self.roomNumber
		yield 'clinic_id', self.clinic_id

# Initializes the database
db.create_all()
