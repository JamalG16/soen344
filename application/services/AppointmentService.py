from application.services import RoomScheduleService, DoctorScheduleService
from application.services.PatientService import canBookAnnual, updateAnnual
from application.TDG import AppointmentTDG
import datetime


def createAppointment(room, doctor_permit_number, patient_hcnumber, length, time, date):
	dateSplit = date.split("-")
	date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
	AppointmentTDG.create(room=room, doctor_permit_number=doctor_permit_number, patient_hcnumber=patient_hcnumber, length=length, time=time, date=date)
	return True

# find if a room is available and if a doctor is available to book an appointment.
# If so, book, the room and doctor at the specified time, with the specified patient, for a type of appointment.
# If the type is to be annual, the patient's last annual must be checked to validate the new annual (at least 1 year difference).
# Also, if the type is annual, check that the next two timeslots can be booked in the same room with the same doctor.
def bookAppointment(patient_hcnumber, length, time, date):
	if length == '20': #checkup
		available_doctor = DoctorScheduleService.findDoctorAtTime(date, time)
		if available_doctor is None:
			return False
		available_room = RoomScheduleService.findRoomAtTime(time=time, date=date)
		if available_room is None:
			return False
		DoctorScheduleService.makeTimeSlotUnavailable(available_doctor, date, time)
		RoomScheduleService.makeTimeSlotUnavailable(available_room, date, time)
		createAppointment(available_room, available_doctor, patient_hcnumber, length, time, date)
		return True
	elif length == '60': #annual
		if not canBookAnnual(patient_hcnumber):
			return False
		available_doctor = DoctorScheduleService.findDoctorForAnnual(date, time)
		if available_doctor is None:
			return False
		available_room = RoomScheduleService.findRoomForAnnual(date, time)
		if available_room is None:
			return False

		DoctorScheduleService.makeTimeSlotUnavailableAnnual(available_doctor, date, time)
		RoomScheduleService.makeTimeSlotUnavailableAnnual(available_room, date, time)

		if createAppointment(available_room, available_doctor, patient_hcnumber, length, time, date):
			updateAnnual(patient_hcnumber, date)
		return True
	else:
		return False

# gets the appointment based on id
def getAppointment(id):
	appointment = AppointmentTDG.find(id)
	if appointment is None:
		return None
	else:
		return dict(appointment)

# gets all patient's appointments. Returns an array, where each value contains an appointment in the form of a dict.
def getAppointments(patient_hcnumber):
	apps = []
	appointments = AppointmentTDG.findAll(patient_hcnumber=patient_hcnumber)
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
		date = appointment['date']
		time = appointment['time']
		if appointment['length'] == 20:
			DoctorScheduleService.makeTimeSlotAvailable(doctor, date, time)
			RoomScheduleService.makeTimeSlotAvailable(room, date, time)
			AppointmentTDG.delete(appointment['id'])
			return True
		elif appointment['length'] == 60:
			DoctorScheduleService.makeTimeSlotAvailableAnnual(doctor, date, time)
			RoomScheduleService.makeTimeSlotAvailableAnnual(room, date, time)
			AppointmentTDG.delete(appointment['id'])
			return True
		else:
			return False

#updates the information of an appointment
def updateDB(id, room, doctor_permit_number, length, time, date):
	dateSplit = date.split("-")
	date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
	AppointmentTDG.update(id=id, room=room, doctor_permit_number=doctor_permit_number, length=length, time=time, date=date)

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
			available_doctor = DoctorScheduleService.findDoctorAtTime(date,time)
			if available_doctor is None:
				return False
			available_room = RoomScheduleService.findRoomAtTime(time=time, date=date)
			if available_room is None:
				return False
			DoctorScheduleService.makeTimeSlotAvailable(appointment['doctor_permit_number'], appointment['date'], appointment['time'])
			RoomScheduleService.makeTimeSlotAvailable(appointment['room'], appointment['date'], appointment['time'])
			DoctorScheduleService.makeTimeSlotUnavailable(available_doctor, date, time)
			RoomScheduleService.makeTimeSlotUnavailable(available_room, date, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)
		elif appointment['length'] == 20 and length=='60':
			available_doctor = DoctorScheduleService.findDoctorForAnnual(time=time, date=date)
			if available_doctor is None:
				return False
			available_room = RoomScheduleService.findRoomForAnnual(date, time)
			if available_room is None:
				return False
			if not canBookAnnual(patient_hcnumber):
				return False
			DoctorScheduleService.makeTimeSlotAvailable(appointment['doctor_permit_number'], appointment['date'], appointment['time'])
			RoomScheduleService.makeTimeSlotAvailable(appointment['room'], appointment['date'], appointment['time'])
			DoctorScheduleService.makeTimeSlotUnavailableAnnual(available_doctor, date, time)
			RoomScheduleService.makeTimeSlotUnavailableAnnual(available_room, date, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)

		elif appointment['length'] == 60 and length=='20':
			available_doctor = DoctorScheduleService.findDoctorAtTime(time=time, date=date)
			if available_doctor is None:
				return False
			available_room = RoomScheduleService.findRoomAtTime(time=time, date=date)
			if available_room is None:
				return False
			DoctorScheduleService.makeTimeSlotAvailableAnnual(appointment['doctor_permit_number'], appointment['date'], appointment['time'])
			RoomScheduleService.makeTimeSlotAvailableAnnual(appointment['room'], appointment['date'], appointment['time'])
			DoctorScheduleService.makeTimeSlotUnavailable(available_doctor, date, time)
			RoomScheduleService.makeTimeSlotUnavailable(available_room, date, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor, length, time, date)
		elif appointment['length'] == 60 and length == '60':
			available_doctor = DoctorScheduleService.findDoctorForAnnual(time=time, date=date)
			if available_doctor is None:
				return False
			available_room = RoomScheduleService.findRoomForAnnual(time=time, date=date)
			if available_room is None:
				return False
			DoctorScheduleService.makeTimeSlotAvailableAnnual(appointment['doctor_permit_number'], appointment['date'], appointment['time'])
			RoomScheduleService.makeTimeSlotAvailableAnnual(appointment['room'], appointment['date'], appointment['time'])
			DoctorScheduleService.makeTimeSlotUnavailableAnnual(available_doctor, date, time)
			RoomScheduleService.makeTimeSlotUnavailableAnnual(available_room, date, time)
			#updates
			updateDB(appointment['id'], available_room, available_doctor,length, time, date)
		return True