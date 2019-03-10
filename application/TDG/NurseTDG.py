from application.models.Nurse import Nurse
from index import db

# Returns patient if found
def find(access_ID):
	return Nurse.query.filter_by(access_ID=access_ID).first()

def create(access_ID, fname, lname, password_hash):
    # Create the new nurse
    newNurse = Nurse(access_ID=access_ID, fname=fname, lname=lname, password_hash=password_hash)
    # Add it to the database
    db.session.add(newNurse)
    # Commit it
    db.session.commit()
