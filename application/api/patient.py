'''
This file documents the api routes for patient related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.services import PatientService
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls 
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
patient = Blueprint('patient', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index 
@patient.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@patient.route('/api/patient/', methods=['PUT'])
def newPatient():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False

	# Create a patient and find our whether it is successful or not
	success = PatientService.createPatient(hcnumber=data['hcnumber'], fname=data['fname'], lname=data['lname'], birthday=data['birthday'], gender=data['gender'], phone=data['phone'], email=data['email'], address=data['address'], password=data['password'], lastAnnual=data['lastAnnual'])
	if success:
		message = "Patient has been created"
	else:
		message = "Patient already exists"

	response = json.dumps({"success":success, "message":message})
	return response

@patient.route('/api/patient/authenticate/', methods=httpMethods)
def userAuthenticate():

	# convert request data to dictionary
	data = toDict(request.data)

	success = False  
	message = "" 
	status = ""  # OK, DENIED, WARNING
	response = {}  
	user = {}

	# logging in
	
	# check if health card number exists
	success = PatientService.patientExists(data['hcnumber'])
	# Verify User  
	success = PatientService.authenticate(data['hcnumber'], data['password'])
	
	# if health card number exists & authenticated, then get the patient
	if success:
		user = PatientService.getPatient(data['hcnumber'])
		# convert datetimes to strings
		user['birthday'] = user['birthday'].strftime("%Y-%m-%d")
		if user['lastAnnual'] is not None:
			user['lastAnnual'] = user['lastAnnual'].strftime("%Y-%m-%d")
		message = "Patient authenticated."
		status = "OK"
		response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
	# else the user is not authenticated, request is denied
	else:
		message = "User not authenticated."
		status = "DENIED"

	response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
	return response

