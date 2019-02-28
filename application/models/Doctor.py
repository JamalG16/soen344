from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

class Doctor(db.Model):
	permit_number = db.Column(db.String(50), nullable=False)
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	specialty = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(100), nullable=False)
	city = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return '<Doctor %r %r>' % self.fname % self.lname

	# to iterate over a patient to retrieve specific attributes
	def __iter__(self):
		yield 'permit_number', self.permit_number
		yield 'fname', self.fname
		yield 'lname', self.lname	
		yield 'specialty', self.specialty
		yield 'password_hash', self.password_hash
		yield 'city', self.city

# Initializes the database
db.create_all()

# Returns True if doctor exists
def doctorExists(permit_number):
	return Doctor.query.filter_by(permit_number=permit_number).first() is not None

# Returns True if doctor is created
def createDoctor(permit_number, fname, lname, specialty, password, city):
	reponse = False
	if doctorExists(permit_number):
		reponse =  False # if doctor exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)

		# Create the new doctor
		newDoctor = Doctor(permit_number=permit_number, fname=fname, lname=lname, password_hash=password_hash, specialty=specialty, city=city)

		# Add it to the database
		db.session.add(newDoctor)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse







