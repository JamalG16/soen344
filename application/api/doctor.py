'''
This file documents the api routes for the login information. It maps api calls that will return the patient

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Doctor
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls 
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
doctor = Blueprint('doctor', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index 
@doctor.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@doctor.route('/api/doctor/', methods=['PUT','GET'])
def newDoctor():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	if request.method == 'PUT':

		# Create a doctor and find our whether it is successful or not
		success = Doctor.createDoctor(permit_number=data['permit_number'], fname=data['fname'], lname=data['lname'], specialty=data['specialty'], password=data['password'], city=data['city'])
		
		if success:
			message = "Doctor has been created"
		else:
			message = "Doctor already exists"

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message})
	return response

@doctor.route('/api/doctor/authenticate/', methods=httpMethods)
def userAuthenticate():

	# convert request data to dictionary
	data = toDict(request.data)

	success = False  
	message = "" 
	status = ""  # OK, DENIED, WARNING
	response = {}  
	user = {}
	
	# logging in
	if request.method == 'POST':
		# check if permit number exists
		success = Doctor.doctorExists(data['permit_number'])
		# Verify User  
		success = Doctor.authenticate(data['permit_number'], data['password'])

		# if permit number exists & authenticated, then get the patient
		if success:
			user = Doctor.getDoctor(data['permit_number'])
			# convert datetimes to strings
			message = "Doctor authenticated."
			status = "OK"
			response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
		# else the user is not authenticated, request is denied
		else:
			message = "User not authenticated."
			status = "DENIED"

	else:
		message = "HTTP method invalid."
		status = "WARNING"
		success = False

	response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
	return response

