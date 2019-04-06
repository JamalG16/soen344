from application.models.Appointment import Appointment
from index import db

# Returns appointment if found
def find(id):
	return Appointment.query.filter_by(id=id).first()

# returns all appointments of a patient
def findAll(patient_hcnumber):
    return Appointment.query.filter_by(patient_hcnumber=patient_hcnumber).all()

# returns all appointments for a doctor
def findForDoctor(doctor_permit_number):
    return Appointment.query.filter_by(doctor_permit_number=doctor_permit_number).all()

#returns all appointments for clinics
def findAppointments(clinic_id):
    return Appointment.query.filter_by(clinic_id=clinic_id)

# create appointment
def create(room, clinic_id, doctor_permit_number, patient_hcnumber, length, time, date):
    newAppointment = Appointment(room=room, clinic_id=clinic_id, doctor_permit_number=doctor_permit_number, patient_hcnumber=patient_hcnumber, length=length, time=time, date=date)
    # Add it to the database
    db.session.add(newAppointment)
	# Commit it
    db.session.commit()
    return True

# deletes an appointment by id
def delete(id):
    Appointment.query.filter_by(id=id).delete()
    db.session.commit()

# updates an appointment in DB
def update(id, room, clinic_id, doctor_permit_number, length, time, date):
    Appointment.query.filter_by(id=id).first().doctor_permit_number = doctor_permit_number
    Appointment.query.filter_by(id=id).first().room = room
    Appointment.query.filter_by(id=id).first().clinic_id = clinic_id
    Appointment.query.filter_by(id=id).first().length = length
    Appointment.query.filter_by(id=id).first().time = time
    Appointment.query.filter_by(id=id).first().date = date
    db.session.commit()