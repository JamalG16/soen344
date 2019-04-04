'''
This file documents the api routes for doctor related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Doctor
from application.services import DoctorService, DoctorScheduleService
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
from ..models import DoctorSchedule
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


@doctor.route('/api/doctor/', methods=['PUT'])
def newDoctor():
    data = request.data
    data = data.decode('utf8').replace("'",'"')
    data = json.loads(data)
    print(data)
    success = False

    # Create a doctor and find our whether it is successful or not
    success = DoctorService.createDoctor(permit_number=data['permit_number'], fname=data['fname'], lname=data['lname'], specialty=data['specialty'], password=data['password'], city=data['city'])

    if success:
        message = "Doctor has been created"
    else:
        message = "Doctor already exists"

    response = json.dumps({"success":success, "message":message})
    return response


@doctor.route('/api/doctor/authenticate/', methods=['POST'])
def userAuthenticate():

    # convert request data to dictionary
    data = toDict(request.data)

    success = False
    message = ""
    status = ""  # OK, DENIED, WARNING
    response = {}
    user = {}

    # check if permit number exists
    success = DoctorService.doctorExists(data['permit_number'])
    # Verify User
    success = DoctorService.authenticate(data['permit_number'], data['password'])

    # if permit number exists & authenticated, then get the patient
    if success:
        user = DoctorService.getDoctor(data['permit_number'])
        # convert datetimes to strings
        message = "Doctor authenticated."
        status = "OK"
        response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
    # else the user is not authenticated, request is denied
    else:
        message = "User not authenticated."
        status = "DENIED"

    response = json.dumps({'success': success, 'status': status, 'message': message,'user':user})
    return response


@doctor.route('/api/doctor/availability/', methods=['POST'])
def setAvailability():
    # convert request data to dictionary
    data = toDict(request.data)

    success = False
    message = ""
    status = ""  # OK, DENIED, WARNING
    response = {}
    user = {}

    # check if permit number exists
    success = DoctorService.doctorExists(data['permit_number'])
    # Verify User
    success = DoctorService.verifyHash(data['permit_number'], data['password_hash'])

    # if permit number exists & authenticated, then get the patient
    if success:
        returned = DoctorScheduleService.setAvailability(data['permit_number'], data["date"], data["timeslots"],
                                                         data["clinic_id"])
        message = returned['message']
        if returned['success']:
            status = "OK"
        else:
            status = "DENIED"

        response = json.dumps({'success': success, 'status': status, 'message': message, 'user': user})
    # else the user is not authenticated, request is denied
    else:
        message = "User not authenticated."
        status = "DENIED"

    response = json.dumps({'success': success, 'status': status, 'message': message, 'user': user})
    return response


@doctor.route('/api/doctor/availability/', methods=['GET'])
def getAvailability():
    # convert request data to dictionary
    data = request.args

    success = False
    message = ""
    status = ""  # OK, DENIED, WARNING
    response = {}
    user = {}
    returned_values = {'timeslot': '', 'clinics': ''}

    # check if permit number exists
    success = DoctorService.doctorExists(data['permit_number']) and \
        DoctorService.verifyHash(data['permit_number'], data['password_hash'])

    # if permit number exists & authenticated, then get the patient
    if success:
        returned_values = DoctorScheduleService.getAvailability(data['permit_number'], data['date'])
        # convert datetimes to strings
        message = "schedule found."
        status = "OK"
        response = json.dumps({'success': success, 'status': status, 'message': message, 'user': user})
    # else the user is not authenticated, request is denied
    else:
        message = "User not authenticated or does not exist."
        status = "DENIED"

    response = json.dumps({'success': success, 'status': status, 'message': message,
                           'schedule': returned_values['timeslot'], 'clinics': returned_values['clinics']})
    return response

@doctor.route('/api/doctor/find/', methods=['POST'])
def userFind():

    # convert request data to dictionary
    data = toDict(request.data)

    success = False
    message = ""
    status = ""  # OK, DENIED, WARNING
    response = {}

    # check if permit number exists
    success = DoctorService.doctorExists(data['permit_number'])

    # if permit number exists & authenticated, then get the patient
    if success:
        message = "Doctor found."
        status = "OK"
        response = json.dumps({'success': success, 'status': status, 'message': message})
    # else the user is not authenticated, request is denied
    else:
        message = "Doctor not found."
        status = "DENIED"

    response = json.dumps({'success': success, 'status': status, 'message': message})
    return response