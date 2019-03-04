from index import db
from .Appointment import Appointment

# PickleType coverts python object to a string so that it can be stored on the database
class Checkup(Appointment):

    def __init__(self, length):
        self.length = 20

    def __iter__(self):
        yield 'room', self.room
        yield 'timeSlot', self.timeSlot
        yield 'doctor', self.doctor
        yield 'patient', self.patient
        yield 'length', self.length

def createAppointment(room, timeSlot, doctor, patient, length):
	# Create the new appointment
    newAppointment = Appointment(room=room, timeSlot=timeSlot, doctor=doctor, patient=patient, length=Checkup.length)
	# Add it to the database
    db.session.add(newAppointment)
    # Commit it
    db.session.commit()
    return True

