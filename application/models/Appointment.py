from index import db
from .Room import roomAvailable, findRoomAtTime, findRoomForAnnual
from .Doctor import findDoctorAtTime, findDoctorForAnnual
from .Patient import canBookAnnual, updateAnnual
from .DoctorSchedule import makeUnavailable, makeAvailable, getNextTimeSlot, makeAvailableAnnual, makeUnavailableAnnual
import datetime

# PickleType coverts python object to a string so that it can be stored on the database
class Appointment(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	room = db.Column(db.Integer, db.ForeignKey('room.roomNumber'), nullable=False)
	doctor_permit_number = db.Column(db.String(7), db.ForeignKey('doctor.permit_number'), nullable=False)
	patient_hcnumber = db.Column(db.String(12), db.ForeignKey('patient.hcnumber'), nullable=False)
	length = db.Column(db.Integer, nullable=False)
	time = db.Column(db.String(), nullable=False)
	date = db.Column(db.Date(), nullable=False)

	def __iter__(self):
		yield 'id', self.id
		yield 'room', self.room
		yield 'doctor_permit_number', self.doctor_permit_number
		yield 'patient_hcnumber', self.patient_hcnumber
		yield 'length', self.length
		yield 'time', self.time
		yield 'date', self.date.strftime("%Y-%m-%d")

# Initializes the database
db.create_all()

def createAppointment(room, doctor_permit_number, patient_hcnumber, length, time, date):
	dateSplit = date.split("-")
	date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
	newAppointment = Appointment(room=room, doctor_permit_number=doctor_permit_number, patient_hcnumber=patient_hcnumber, length=length, time=time, date=date)
	# Add it to the database
	db.session.add(newAppointment)
	# Commit it
	db.session.commit()
	return True

# find if a room is available and if a doctor is available to book an appointment. 
# If so, book, the room and doctor at the specified time, with the specified patient, for a type of appointment.
# If the type is to be annual, the patient's last annual must be checked to validate the new annual (at least 1 year difference).
# Also, if the type is annual, check that the next two timeslots can be booked in the same room with the same doctor.
def bookAppointment(patient_hcnumber, length, time, date):
	if length == '20': #checkup
		available_doctor = findDoctorAtTime(time)
		if available_doctor is None:
			return False
		available_room = findRoomAtTime(time)
		if available_room is None:
			return False
		makeUnavailable(available_doctor, time)
		makeUnavailable(available_room, time)
		createAppointment(available_room, available_doctor, patient_hcnumber, length, time, date)
		return True
	elif length == '60': #annual
		if not canBookAnnual(patient_hcnumber):
			return False
		available_doctor = findDoctorForAnnual(time)
		if available_doctor is None:
			return False
		available_room = findRoomForAnnual(time)
		if available_room is None:
			return False
		
		makeUnavailableAnnual(available_room, time)
		makeUnavailableAnnual(available_doctor, time)

		if createAppointment(available_room, available_doctor, patient_hcnumber, length, time, date):
			updateAnnual(patient_hcnumber, date)
		return True
	else:
		return False

# gets the appointment based on id
def getAppointment(id):
	appointment = Appointment.query.filter_by(id=id).first()
	if appointment is None:
		return None
	else:
		return dict(appointment)

# gets all patient's appointments. Returns an array, where each value contains an appointment in the form of a dict.
def getAppointments(patient_hcnumber):
	apps = []
	appointments = Appointment.query.filter_by(patient_hcnumber=patient_hcnumber).all()
	for appointment in appointments:
		apps.append(dict(appointment))
	return apps

# cancels an appointment and frees the time slots
def cancelAppointment(id):
	appointment = getAppointment(id)
	if appointment is None:
		return False
	else:
		doctor = appointment['doctor_permit_number']
		room = appointment['room']
		time = appointment['time']
		if appointment['length'] == 20:
			makeAvailable(doctor, time)
			makeAvailable(room, time)
			Appointment.query.filter_by(id = appointment['id']).delete()
			db.session.commit()
			return True
		elif appointment['length'] == 60:
			makeAvailableAnnual(doctor, time)
			makeAvailableAnnual(room, time)
			Appointment.query.filter_by(id=appointment['id']).delete()
			db.session.commit()
			return True
		else:
			return False

#updates the information of an appointment
def updateDB(id, room, doctor_permit_number, length, time, date):
	dateSplit = date.split("-")
	date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
	Appointment.query.filter_by(id=id).first().doctor_permit_number = doctor_permit_number
	Appointment.query.filter_by(id=id).first().room = room
	Appointment.query.filter_by(id=id).first().length = length
	Appointment.query.filter_by(id=id).first().time = time
	Appointment.query.filter_by(id=id).first().date = date
	db.session.commit()

#gets the currently made appointment and tries to change it to the new appointment parameters.
# 4 cases: 20mins --> 20mins, 20mins-->60mins, 60mins-->20mins, 60mins-->60mins
def updateAppointment(id, patient_hcnumber, length, time, date):
	appointment = getAppointment(id)
	if appointment is None:
		return False
	elif appointment['time'] == time and appointment['length'] == int(length): #trying to book at same time for same length
		return False
	else:
		if appointment['length'] == 20 and length =='20':
			available_doctor = findDoctorAtTime(time)
			if available_doctor is None:
				return False
			available_room = findRoomAtTime(time)
			if available_room is None:
				return False
			makeAvailable(appointment['doctor_permit_number'], appointment['time'])
			makeAvailable(appointment['room'],appointment['time'])
			makeUnavailable(available_doctor, time)
			makeUnavailable(available_room, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)
		elif appointment['length'] == 20 and length=='60':
			available_doctor = findDoctorForAnnual(time)
			if available_doctor is None:
				return False
			available_room = findRoomForAnnual(time)
			if available_room is None:
				return False
			if not canBookAnnual(patient_hcnumber):
				return False
			makeAvailable(appointment['doctor_permit_number'], appointment['time'])
			makeAvailable(appointment['room'],appointment['time'])
			makeUnavailableAnnual(available_doctor, time)
			makeUnavailableAnnual(available_room, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)

		elif appointment['length'] == 60 and length=='20':
			available_doctor = findDoctorAtTime(time)
			if available_doctor is None:
				return False
			available_room = findRoomAtTime(time)
			if available_room is None:
				return False
			makeAvailableAnnual(appointment['doctor_permit_number'], appointment['time'])
			makeAvailableAnnual(appointment['room'],appointment['time'])
			makeUnavailable(available_doctor, time)
			makeUnavailable(available_room, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)
		elif appointment['length'] == 60 and length == '60':
			available_doctor = findDoctorForAnnual(time)
			if available_doctor is None:
				return False
			available_room = findRoomForAnnual(time)
			if available_room is None:
				return False
			makeAvailableAnnual(appointment['doctor_permit_number'], appointment['time'])
			makeAvailableAnnual(appointment['room'],appointment['time'])
			makeUnavailableAnnual(available_doctor, time)
			makeUnavailableAnnual(available_room, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor,length, time, date)
		return True