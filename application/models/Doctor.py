from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

class Doctor(db.Model):
	permit_number = db.Column(db.String(7), nullable=False, primary_key=True)
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

# Returns true if doctor is authenticated
def authenticate(permit_number, password):
	verified = False
	user = getDoctor(permit_number)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified

# Returns Doctor if found
def getDoctor(permit_number):
	doctor = Doctor.query.filter_by(permit_number=permit_number).first()
	if doctor is None:
		return None
	else:
		return dict(doctor)

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

# TO DO
def hasDoctor(time):
	return True