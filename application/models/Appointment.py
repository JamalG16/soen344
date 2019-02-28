from index import db

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
    pass
