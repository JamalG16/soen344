from index import db
import datetime


# PickleType coverts python object to a string so that it can be stored on the database
class Appointment(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	room = db.Column(db.Integer, db.ForeignKey('room.roomNumber'), nullable=False)
	clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
	doctor_permit_number = db.Column(db.String(7), db.ForeignKey('doctor.permit_number'), nullable=False)
	patient_hcnumber = db.Column(db.String(12), db.ForeignKey('patient.hcnumber'), nullable=False)
	length = db.Column(db.Integer, nullable=False)
	time = db.Column(db.String(), nullable=False)
	date = db.Column(db.Date(), nullable=False)

	def __iter__(self):
		yield 'id', self.id
		yield 'room', self.room
		yield 'clinic_id', self.clinic_id
		yield 'doctor_permit_number', self.doctor_permit_number
		yield 'patient_hcnumber', self.patient_hcnumber
		yield 'length', self.length
		yield 'time', self.time
		yield 'date', self.date.strftime("%Y-%m-%d")

# Initializes the database
db.create_all()