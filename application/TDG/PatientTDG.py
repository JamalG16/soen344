from application.models.Patient import Patient
from index import db

# Returns patient if found
def find(hcnumber):
	return Patient.query.filter_by(hcnumber=hcnumber).first()

def create(hcnumber, fname, lname, birthday, gender, phone, email, address, password_hash, lastAnnual):
   # Create the new patient
    newPatient = Patient(hcnumber=hcnumber, fname=fname, lname=lname, birthday=birthday, gender=gender, phone=phone, email=email, address=address, password_hash=password_hash, lastAnnual=lastAnnual)
    # Add it to the database
    db.session.add(newPatient)
    # Commit it
    db.session.commit()

# updates user's last annual date (NOT TESTED)
def update(hcnumber, date):
    Patient.query.filter_by(hcnumber=hcnumber).first().lastAnnual = date
    db.session.commit()
