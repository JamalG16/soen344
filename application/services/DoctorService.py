from application.TDG import DoctorTDG
from passlib.hash import sha256_crypt

# Returns True if doctor exists
def doctorExists(permit_number):
	return DoctorTDG.find(permit_number) is not None

# Returns true if doctor is authenticated
def authenticate(permit_number, password):
	verified = False
	user = getDoctor(permit_number)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified

# Returns Doctor if found
def getDoctor(permit_number):
	doctor = DoctorTDG.find(permit_number)
	if doctor is None:
		return None
	else:
		return dict(doctor)

def getAllDoctors():
	return DoctorTDG.findAll()

def getAllDoctorPermits():
	doctor_permit_numbers = []
	for row in getAllDoctors():
		doctor_permit_numbers.append(row.permit_number)
	return doctor_permit_numbers

# Returns True if doctor is created
def createDoctor(permit_number, fname, lname, specialty, password, city):
	reponse = False
	if doctorExists(permit_number):
		reponse =  False # if doctor exists then return false
	else:
		# hash password
		password_hash = sha256_crypt.hash(password)
		# Create the new doctor
		DoctorTDG.create(permit_number=permit_number, fname=fname, lname=lname, password_hash=password_hash, specialty=specialty, city=city)
		reponse = True
	return reponse
