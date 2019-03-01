'''
This file documents the api routes for the login information. It maps api calls that will return the patient

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Room
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls 
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
room = Blueprint('room', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index 
@room.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@room.route('/api/room/', methods=['PUT','GET'])
def newRoom():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
    
	if request.method == 'PUT':

		success = Room.createRoom(roomNumber=data['roomNumber'])
		if success:
			message = "Room has been created"
		else:
			message = "Room already exists"
	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message})
	return response
