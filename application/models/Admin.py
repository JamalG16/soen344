from index import db
from passlib.hash import sha256_crypt

class Admin(db.Model):
	username = db.Column(db.String(30), primary_key=True)
	password_hash = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<admin %r>' % self.username

	# to iterate over an admin
	def __iter__(self):
		yield 'username', self.username
		yield 'password_hash', self.password_hash


# Initializes the database
db.create_all()

# Returns True if admin exists
def adminExists(username):
	return Admin.query.filter_by(username=username).first() is not None

# Returns true if admin is authenticated
def authenticate(username, password):
	verified = False
	admin = getAdmin(username)
	if admin is not None:
		verified = sha256_crypt.verify(password, admin['password_hash'])

	return verified

# Returns admin if found
def getAdmin(username):
	admin = Admin.query.filter_by(username=username).first()
	if admin is None:
		return None
	else:
		return dict(admin)

# Returns True if admin is created
def createAdmin(username, password):
	reponse = False
	if adminExists(username):
		reponse =  False # if admin exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)

		# Create the new admin
		newAdmin = Admin(username=username, password_hash=password_hash)

		# Add it to the database
		db.session.add(newAdmin)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse







