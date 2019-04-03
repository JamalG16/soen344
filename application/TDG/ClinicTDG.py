from application.models.Clinic import Clinic
from index import db

# Returns clinic if found
def find(id):
	return Clinic.query.filter_by(id=id).first()

def findByData(name, address):
    return Clinic.query.filter_by(name=name, address=address).first()

# returns all clinics
def findAll():
    return Clinic.query.all()

def create(name, address):
    newClinic = Clinic(name=name, address=address)
    # Add it to the database
    db.session.add(newClinic)
	# Commit it
    db.session.commit()

def delete(id):
    Clinic.query.filter_by(id=id).delete()
    db.session.commit()

# updates an clinic in DB
def update(id, name, address):
    Clinic.query.filter_by(id=id).first().name = name
    Clinic.query.filter_by(id=id).first().address = address
    db.session.commit()