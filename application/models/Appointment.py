from index import db
from .Room import roomAvailable
from .Doctor import hasDoctor
from .Patient import hasPatient

# PickleType coverts python object to a string so that it can be stored on the database
class Appointment(db.Model):
    room = db.Column(db.PickleType(mutable=True), primary_key=True)
    timeSlot = db.Column(db.PickleType(mutable=True), nullable=False)
    doctor = db.Column(db.PickleType(mutable=True), nullable=False)
    patient = db.Column(db.PickleType(mutable=True), nullable=False)
    length = db.Column(db.PickeType(mutable=True), nullable=False)

    def __iter__(self):
        yield 'room', self.room
        yield 'timeSlot', self.timeSlot
        yield 'doctor', self.doctor
        yield 'patient', self.patient
        yield 'length', self.length
    
def createAppointment(room, timeSlot, doctor, patient, length):
	reponse = False
	if (not roomAvailable(room, timeSlot) or not hasDoctor(timeSlot) or hasPatient(timeSlot)):
		reponse =  False 
	else:
		# Create the new appointment
		newAppointment = Appointment(room=room, timeSlot=timeSlot, doctor=doctor, patient=patient, length=length)

		# Add it to the database
		db.session.add(newAppointment)

		# Commit it
		db.session.commit()

		reponse = True
	return reponse
			
