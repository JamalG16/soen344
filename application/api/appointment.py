'''
This file documents the api routes for the login information. It maps api calls that will return the patient

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Appointment, Checkup, Annual, Doctor, Room, Schedule, Patient
from application.models.Checkup import createAppointment
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

@appointment.route('/api/appointment/book', methods=['PUT','GET'])
def newAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	info =None
	if request.method == 'PUT':
		success = Appointment.book(data['hcnumber'], data['length'], data['time'], data['date'])
		if success:
			message = "Appointmented has been created"
		else:
			message = "Appointment already exists or there are no doctors/rooms available. If annual appointment, may not have been a year yet."

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message, "info":info})
	return response

@appointment.route('/api/appointment/check', methods=['PUT','GET'])
def checkAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	booking = {}
	if request.method == 'POST':
		booking = Appointment.getBooking(data['hcnumber'])
		if booking is not None:
			success = True
			booking['date'] = booking['date'].strftime("%Y-%m-%d")
		else:
			success = False

		if success:
			message = "Appointment(s) retrieved."
		else:
			message = "No appointment(s) retrieved."

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message, "booking":booking})
	return response

#TO DO
@appointment.route('/api/appointment/cancel', methods=['PUT','GET'])
def cancelAppointment():
	pass
	
# TO DO
@appointment.route('/api/appointment/update', methods=['PUT','GET'])
def updateAppointment():
	pass
