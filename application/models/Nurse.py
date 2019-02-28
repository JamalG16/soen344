from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

class Nurse(db.Model):
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	password_hash = db.Column(db.String(100), nullable=False)
	access_ID = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<Nurse %r %r>' % self.fname % self.lname

	


# Initializes the database
db.create_all()

# Returns True if nurse exists
def nurseExists(access_ID):
	return Nurse.query.filter_by(access_ID=access_ID).first() is not None

# Returns True if nurse is created
def createNurse(fname, lname, password, access_ID):
	reponse = False
	if nurseExists(hcnumber):
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







