from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

class Patient(db.Model):
	hcnumber = db.Column(db.String(12), primary_key=True)
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	birthday = db.Column(db.String(10), nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	phone = db.Column(db.String(10), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	address = db.Column(db.String(120), nullable=False)
	password_hash = db.Column(db.String(100), nullable=False)
	lastAnnual = db.Column(db.String(10), nullable=True)

	def __repr__(self):
		return '<Patient %r %r>' % self.fname % self.lname

	# to iterate over a patient to retrieve specific attributes
	def __iter__(self):
		yield 'hcnumber', self.hcnumber
		yield 'fname', self.fname
		yield 'lname', self.lname
		yield 'birthday', self.birthday
		yield 'gender', self.gender
		yield 'phone', self.phone
		yield 'email', self.email
		yield 'address', self.address
		yield 'password_hash', self.password_hash
		yield 'lastAnnual', self.lastAnnual


# Initializes the database
db.create_all()

# Returns True if patient exists
def patientExists(hcnumber):
	return Patient.query.filter_by(hcnumber=hcnumber).first() is not None

# Returns true if patient is authenticated
def authenticate(hcnumber, password):
	verified = False
	user = getPatient(hcnumber)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified

# Returns Patient if found
def getPatient(hcnumber):
	patient = Patient.query.filter_by(hcnumber=hcnumber).first()
	if patient is None:
		return None
	else:
		return dict(patient)

# Returns True if patient is created
def createPatient(hcnumber, fname, lname, birthday, gender, phone, email, address, password, lastAnnual):
	reponse = False
	if patientExists(hcnumber):
		reponse =  False # if patient exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)

		# Create the new patient
		newPatient = Patient(hcnumber=hcnumber, fname=fname, lname=lname, birthday=birthday, gender=gender, phone=phone, email=email, address=address, password_hash=password_hash, lastAnnual=lastAnnual)

		# Add it to the database
		db.session.add(newPatient)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse







