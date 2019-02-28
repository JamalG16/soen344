from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

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

# Returns True if nurse exists
def nurseExists(access_ID):
	return Nurse.query.filter_by(access_ID=access_ID).first() is not None

# Returns true if nurse is authenticated
def authenticate(access_ID, password):
	verified = False
	user = getNurse(access_ID)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified

# Returns nurse if found
def getNurse(access_ID):
	nurse = Nurse.query.filter_by(access_ID=access_ID).first()
	if nurse is None:
		return None
	else:
		return dict(nurse)
		
# Returns True if nurse is created
def createNurse(access_ID, fname, lname, password):
	reponse = False
	if nurseExists(access_ID):
		reponse =  False # if nurse exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)

		# Create the new nurse
		newNurse = Nurse(fname=fname, lname=lname, password_hash=password_hash, access_ID=access_ID)

		# Add it to the database
		db.session.add(newNurse)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse







