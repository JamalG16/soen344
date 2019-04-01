'''
This file documents the api routes for nurse related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.services import NurseService, DoctorService, DoctorScheduleService
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
def newNurse():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False

	# Create a nurse and find our whether it is successful or not
	success = NurseService.createNurse(access_ID=data['access_ID'], fname=data['fname'], lname=data['lname'], password=data['password'])
	if success:
		message = "Nurse has been created"
	else:
		message = "Nurse already exists"


	response = json.dumps({"success":success, "message":message})
	return response

@nurse.route('/api/nurse/authenticate/', methods=['POST'])
def userAuthenticate():

	# convert request data to dictionary
	data = toDict(request.data)

	success = False  
	message = "" 
	status = ""  # OK, DENIED, WARNING
	response = {}  
	user = {}

	# check if access ID exists
	success = NurseService.nurseExists(data['access_ID'])
	# Verify User  
	success = NurseService.authenticate(data['access_ID'], data['password'])

	# if access ID exists & authenticated, then get the patient
	if success:
		user = NurseService.getNurse(data['access_ID'])
		# convert datetimes to strings
		message = "Nurse authenticated."
		status = "OK"
		response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
	# else the user is not authenticated, request is denied
	else:
		message = "User not authenticated."
		status = "DENIED"

	response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
	return response

@nurse.route('/api/nurse/doctorAvailability/', methods=['GET'])
def getDoctorAvailability():
    # convert request data to dictionary
    data = request.args

    success = False
    message = ""
    status = ""  # OK, DENIED, WARNING
    response = {}
    user = {}
    schedule = {}

    # check if permit number exists
    success = DoctorService.doctorExists(data['permit_number'])

    # if permit number exists, get the doctor's timeslots
    if success:
        schedule = DoctorScheduleService.getAvailability(data['permit_number'], data['date'])
        # convert datetimes to strings
        message = "schedule found."
        status = "OK"
        response = json.dumps({'success': success, 'status': status, 'message': message, 'user': user})
    # else the user is not authenticated, request is denied
    else:
        message = "User not authenticated or does not exist."
        status = "DENIED"

    response = json.dumps({'success': success, 'status': status, 'message': message, 'schedule': schedule})
    return response