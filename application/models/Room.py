from index import db
from datetime import datetime

class Room(db.Model):
	roomNumber = db.Column(db.Integer, primary_key=True)

	def __iter__(self):
		yield 'roomNumber', self.roomNumber

# Initializes the database
db.create_all()
