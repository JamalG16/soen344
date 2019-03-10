from application.models.Doctor import Doctor
from index import db

# Returns patient if found
def find(permit_number):
	return Doctor.query.filter_by(permit_number=permit_number).first()

# return all doctors
def findAll():
    return db.session.query(Doctor.permit_number).all()

def create(permit_number, fname, lname, specialty, password_hash, city):
    newDoctor = Doctor(permit_number=permit_number, fname=fname, lname=lname, password_hash=password_hash, specialty=specialty, city=city)
    # Add it to the database
    db.session.add(newDoctor)
	# Commit it
    db.session.commit()
