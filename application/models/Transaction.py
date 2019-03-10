from index import db

# PickleType coverts python object to a string so that it can be stored on the database
class Transaction(db.Model):
    timeSlot = db.Column(db.PickleType(mutable=True), primary_key=True)
    doctor = db.Column(db.PickleType(mutable=True), nullable=False)
    patient = db.Column(db.PickleType(mutable=True), nullable=False)
    appointment = db.Column(db.PickleType(mutable=True), nullable=False)
    room = db.Column(db.PickleType(mutable=True), nullable=False)

    def __iter__(self):
        yield 'timeSlot', self.timeSlot
        yield 'doctor', self.doctor
        yield 'patient', self.patient
        yield 'appointment', self.appointment
        yield 'room', self.room