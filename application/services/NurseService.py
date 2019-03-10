from application.TDG import NurseTDG
from passlib.hash import sha256_crypt

# Returns True if nurse exists
def nurseExists(access_ID):
	return NurseTDG.find(access_ID) is not None

# Returns nurse if found
def getNurse(access_ID):
	nurse = NurseTDG.find(access_ID)
	if nurse is None:
		return None
	else:
		return dict(nurse)

# Returns true if nurse is authenticated
def authenticate(access_ID, password):
	verified = False
	user = getNurse(access_ID)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified
		
# Returns True if nurse is created
def createNurse(access_ID, fname, lname, password):
    reponse = False
    if nurseExists(access_ID):
        reponse =  False # if nurse exists then return false
    else:
        # hash password
        password_hash = sha256_crypt.hash(password)
        NurseTDG.create(access_ID=access_ID, fname=fname, lname=lname, password_hash=password_hash)
        reponse = True
    return reponse