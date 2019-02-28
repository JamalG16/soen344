'''
This file documents the api routes for the login information. It maps api calls that will return the admin

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.models import Admin
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls 
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
admin = Blueprint('admin', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index 
@admin.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@admin.route('/api/admin/', methods=['PUT','GET'])
def newAdmin():
	data = request.data
	data  = data.decode('utf8').replace("'",'"')
	data = json.loads(data)
	print(data)
	success = False
	if request.method == 'PUT':

		# Create an admin and find our whether it is successful or not
		success = Admin.createAdmin(username=data['username'], password=data['password'])
		if success:
			message = "Admin has been created"
		else:
			message = "Admin already exists"

	else:
		success = False
		message = "No HTTP request"

	response = json.dumps({"success":success, "message":message})
	return response

@admin.route('/api/admin/authenticate/', methods=httpMethods)
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
		# check if username exists
		success = Admin.adminExists(data['username'])
		# Verify User  
		success = Admin.authenticate(data['username'], data['password'])

		# if username exists & authenticated, then get the admin
		if success:
			user = Admin.getAdmin(data['username'])
			message = "Admin authenticated."
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

