'''
This file documents the api routes for appointment related events.

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Appointment, Doctor, Room, Patient
from application.services import AppointmentService, DoctorScheduleService, RoomScheduleService
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

	success = AppointmentService.bookAppointment(data['hcnumber'], data['length'], data['time'], data['date'])
	if success:
		message = "Appointment has been created"
	else:
		message = "Appointment already exists or there are no doctors/rooms available. If annual appointment, may not have been a year yet."

	response = json.dumps({"success":success, "message":message, "info":info})
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


# /api/appointment/find?date=<insert_date_here>
@appointment.route('/api/appointment/find', methods=['GET'])
def findAppointments():
	date = request.args.get('date')
	randomRoomNumber=None
	# RoomScheduleService.createTimeSlots(10,date)
	# DoctorScheduleService.createTimeSlots('1234567',date)
	if(date is None):
		message = 'Enter a date to find the appointments for'
		return message, 404
	availableDoctorPermitNumbers = DoctorScheduleService.getAllDoctorsByDate(date)
	print(availableDoctorPermitNumbers)
	availableRoomNumbers = RoomScheduleService.getAllRoomsByDate(date)
	if(availableDoctorPermitNumbers is None):
		message = "Unfortunately there are no doctors avaiable for this date at the moment. Please try later."
		return message, 200
	if(availableRoomNumbers is None):
		import random
		randomRoomNumber = random.randint(0, len(RoomScheduleService.getAllRoomNumbers()))
		RoomScheduleService.createTimeSlots(randomRoomNumber,date)
	listOfAvailableAppointments = AppointmentService.crossCheckDoctorAndRoomList(date,availableDoctorPermitNumbers,RoomScheduleService.getAllRoomNumbers(), randomRoomNumber)
	if listOfAvailableAppointments is None:
		return 204
	else:
		return listOfAvailableAppointments,200
