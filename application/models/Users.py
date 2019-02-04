from index import db
from datetime import datetime
from passlib.hash import sha256_crypt

class User(db.Model):
	hcnumber = db.Column(db.String(12), primary_key=True)
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	birthday = db.Column(db.String(10), nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	phone = db.Column(db.String(10), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	address = db.Column(db.String(120), nullable=False)
	password_hash = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<User %r %r>' % self.username % self.email

	


# Initializes the database
db.create_all()

# Returns True if user exists
def userExists(hcnumber):
	return User.query.filter_by(hcnumber=hcnumber).first() is not None

# Returns True if user is created
def createUser(hcnumber, fname, lname, birthday, gender, phone, email, address, password):
	reponse = False
	if userExists(hcnumber):
		reponse =  False # if user exists then return false
	else:
		# Hash the Password so that we are smart
		password_hash = sha256_crypt.hash(password)

		# Create the new User
		newUser = User(hcnumber=hcnumber, fname=fname, lname=lname, birthday=birthday, gender=gender, phone=phone, email=email, address=address, password_hash=password_hash)

		# Add it 
		db.session.add(newUser)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse







