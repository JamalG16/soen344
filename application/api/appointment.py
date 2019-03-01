'''
This file documents the api routes for the login information. It maps api calls that will return the patient

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Appointment, Checkup, Annual
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

@appointment.route('/api/appointment/', methods=['PUT','GET'])
def newAppointment():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	if request.method == 'PUT':

            if data['length'] == 20:
                success = createAppointment(room=data['room'], timeSlot=data['timeSlot'], doctor=data['doctor'], patient=data['patient'], length=data['length'])
            elif data['length'] == 60:
                success = createAppointment(room=data['room'], timeSlot=data['timeSlot'], doctor=data['doctor'], patient=data['patient'], length=data['length'])
            else:
                success: False
            if success:
                message = "Appointmented has been created"
            else:
                message = "Appointment already exists"

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message})
	return response


