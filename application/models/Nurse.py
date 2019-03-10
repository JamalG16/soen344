from index import db
from datetime import datetime

class Nurse(db.Model):
	access_ID = db.Column(db.String(8), nullable=False, primary_key=True)
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<Nurse %r %r>' % self.fname % self.lname

	# to iterate over a patient to retrieve specific attributes
	def __iter__(self):
		yield 'access_ID', self.access_ID
		yield 'fname', self.fname
		yield 'lname', self.lname	
		yield 'password_hash', self.password_hash

# Initializes the database
db.create_all()