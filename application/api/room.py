'''
This file documents the api routes for room related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Room, DoctorSchedule
from application.models.Room import roomAvailable
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

@room.route('/api/room/', methods=['PUT'])
def newRoom():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False

	success = Room.createRoom(roomNumber=data['roomNumber'])

	if success:
		message = "Room has been created"
	else:
		message = "Room already exists"

	response = json.dumps({"success":success, "message":message})
	return response

@room.route('/api/room/checkAvailability', methods=['POST'])
def checkAvailability():
	# convert request data to dictionary
	data = toDict(request.data)

	success = False  
	message = "" 
	status = ""  # OK, DENIED, WARNING
	response = {}  
	roomAvailability = None

	# check if room number exists
	success = Room.roomExists(data['roomNumber'])
	
	# if room exists, room availabilities
	if success:
		roomAvail = Room.getRoomTimeSlots(data['roomNumber'])
		message = "Room availabilities retrieved."
		status = "OK"
		response = json.dumps({'success': success, 'status': status, 'message': message, 'roomAvail': roomAvailability})
	# else the room doesn't exist and request is denied.
	else:
		message = "Room does not exist."
		status = "DENIED"

	response = json.dumps({'success': success, 'status': status, 'message': message,'roomAvail': roomAvail})
	return response

