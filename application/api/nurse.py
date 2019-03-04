'''
This file documents the api routes for nurse related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Nurse
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls 
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
nurse = Blueprint('nurse', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index 
@nurse.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@nurse.route('/api/nurse/', methods=['PUT'])
def newDoctor():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	if request.method == 'PUT':

		# Create a nurse and find our whether it is successful or not
		success = Nurse.createNurse(access_ID=data['access_ID'], fname=data['fname'], lname=data['lname'], password=data['password'])
		if success:
			message = "Nurse has been created"
		else:
			message = "Nurse already exists"

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message})
	return response

@nurse.route('/api/nurse/authenticate/', methods=httpMethods)
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
		# check if access ID exists
		success = Nurse.nurseExists(data['access_ID'])
		# Verify User  
		success = Nurse.authenticate(data['access_ID'], data['password'])

		# if access ID exists & authenticated, then get the patient
		if success:
			user = Nurse.getNurse(data['access_ID'])
			# convert datetimes to strings
			message = "Nurse authenticated."
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

