from application.TDG import AdminTDG
from passlib.hash import sha256_crypt

# Returns admin if found
def getAdmin(username):
	admin = AdminTDG.find(username)
	if admin is None:
		return None
	else:
		return dict(admin)


# Returns True if admin exists
def adminExists(username):
	return AdminTDG.find(username) is not None

# Returns true if admin is authenticated
def authenticate(username, password):
	verified = False
	admin = getAdmin(username)
	if admin is not None:
		verified = sha256_crypt.verify(password, admin['password_hash'])

	return verified

# Returns True if admin is created
def createAdmin(username, password):
	reponse = False
	if adminExists(username):
		reponse =  False # if admin exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)

		# Create the new admin
		AdminTDG.create(username=username, password_hash=password_hash)

		reponse = True
	return reponse







