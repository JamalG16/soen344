'''
This file documents the api routes for appointment related events.

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Appointment, Doctor, Room, Patient
from application.services import AppointmentService, DoctorScheduleService, RoomScheduleService, RoomService
from application.TDG import RoomScheduleTDG
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
appointment = Blueprint('appointment', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index
@appointment.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@appointment.route('/api/appointment/book', methods=['PUT'])
def newAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	info =None
	message=""
	hello = ""
	#DoctorScheduleService.createTimeSlots('1234567', '2019-04-01')
	#hello = DoctorScheduleService.getTimeSlotsByDateAndDoctor('1234567', '2019-04-01')
	# hello = AppointmentService.bookAppointment(data['hcnumber'], data['length'], data['time'], data['date'])
	#hello = AppointmentService.getAppointment(1)['patient_hcnumber']
	hello = RoomScheduleService.getTimeSlotsByDateAndRoom('123467', '2019-04-01')
	#hello = RoomScheduleTDG.update(10, '2019-04-01', '8:00:false,8:20:true,8:40:true,9:00:true,9:20:true,9:40:true,10:00:true,10:20:true,10:40:true,11:00:true,11:20:true,11:40:true,12:00:true,12:20:true,12:40:true,13:00:true,13:20:true,13:40:true,14:00:true,14:20:true,14:40:true,15:00:true,15:20:true,15:40:true,16:00:true,16:20:true,16:40:true,17:00:true,17:20:true,17:40:true,18:00:true,18:20:true,18:40:true,19:00:true,19:20:true,19:40:true')
	# hello = RoomScheduleTDG.find('2019-04-01', 10).timeSlots
	if success:
		message = "Appointment has been created"
	else:
		message = "Appointment already exists or there are no doctors/rooms available. If annual appointment, may not have been a year yet."

	response = json.dumps({"success":success, "message":message, "info":info, "hello":hello})
	return response

# Returns an array of appointments consisting of the patient specified
@appointment.route('/api/appointment/check', methods=['GET'])
def checkAppointments():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	message=""
	appointments = []

	appointments = AppointmentService.getAppointments(data['hcnumber'])
	if appointments is not None:
		success = True
	else:
		success = False

	if success:
		message = "Appointment(s) retrieved."
	else:
		message = "No appointment(s) retrieved."

	response = json.dumps({"success":success, "message":message, "appointments":appointments})
	return response


@appointment.route('/api/appointment/cancel', methods=['DELETE'])
def cancelAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	cancelled = False
	message = ""

	if AppointmentService.getAppointment(data['id']) is not None:
		success = AppointmentService.cancelAppointment(data['id'])
	if success:
		message= 'Appointment cancelled'
	else:
		message= 'Appointment may not exist or cancellation failed.'

	response = json.dumps({"success":success, "message":message, "cancelled":cancelled})
	return response


@appointment.route('/api/appointment/update', methods=['PUT'])
def updateAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	appointment = None

	if AppointmentService.getAppointment(data['id']) is not None:
		success = AppointmentService.updateAppointment(data['id'], data['hcnumber'], data['length'], data['time'], data['date'])
	if success:
		message = 'Appointment has been updated.'
		appointment = AppointmentService.getAppointment(data['id'])
	else:
		message = 'Appointment has not been updated.'

	response = json.dumps({"success": success, "message":message, "appointment":appointment})
	return response
