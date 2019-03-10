from application.models.Patient import Patient
from application.TDG import PatientTDG
from index import db
from passlib.hash import sha256_crypt
import datetime

# Returns True if patient exists
def patientExists(hcnumber):
	return PatientTDG.find(hcnumber=hcnumber) is not None

# Returns Patient if found
def getPatient(hcnumber):
	patient = PatientTDG.find(hcnumber=hcnumber)
	if patient is None:
		return None
	else:
		return dict(patient)

# Returns true if patient is authenticated
def authenticate(hcnumber, password):
	verified = False
	user = getPatient(hcnumber)
	if user is not None:
		verified = sha256_crypt.verify(password, user['password_hash'])

	return verified

# Returns True if patient is created
def createPatient(hcnumber, fname, lname, birthday, gender, phone, email, address, password, lastAnnual):
    reponse = False
    if patientExists(hcnumber):
        reponse =  False # if patient exists then return false
    else:
        # hash password
        password_hash = sha256_crypt.hash(password)

        # format the dates
        if lastAnnual:
            lastannualSplit = lastAnnual.split("-")
            lastAnnual = datetime.datetime.strptime(lastannualSplit[0] + lastannualSplit[1] + lastannualSplit[2], '%Y%m%d').date()
        else:
            lastAnnual = None

        bdaySplit = birthday.split("-")
        birthday = datetime.datetime.strptime(bdaySplit[0] + bdaySplit[1] + bdaySplit[2], '%Y%m%d').date()

        PatientTDG.create(hcnumber=hcnumber, fname=fname, lname=lname, birthday=birthday, gender=gender, phone=phone, email=email, address=address, password_hash=password_hash, lastAnnual=lastAnnual)
        reponse = True
    return reponse

# Returns true if patient can book an annual appointment. If not, return false.
# Checks when last annual was (must be at least over a year ago).
def canBookAnnual(hcnumber):
	if getPatient(hcnumber)['lastAnnual'] is None:
		return True
	else:
		annual = getPatient(hcnumber)['lastAnnual']
		now = datetime.datetime.now()
		if (now-annual).days >= 365:
			return True
		else:
			return False

# returns true if patient's annual has been changed
# TO DO: update this method to change lastAnnual to the day of the appointment, not the day of the booking
def updateAnnual(hcnumber, date):
	if getPatient(hcnumber) is None:
		return False
	else:
		PatientTDG.update(hcnumber=hcnumber, date=date)
		return True
