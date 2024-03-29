'''
This file documents the api routes for room related events

'''

from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, logging
from index import app
from application.services import ClinicService
from application.util import *
from passlib.hash import sha256_crypt
from application.util import convertRequestDataToDict as toDict
import json

# This is a Blueprint object. We use this as the object to route certain urls
# In /index.py we import this object and attach it to the Flask object app
# This way all the routes attached to this object will be mapped to app as well.
clinic = Blueprint('clinic', __name__)

# list of possible requests
httpMethods = ['PUT', 'GET', 'POST', 'DELETE']

# Index
@clinic.route('/api/', methods=['GET','OPTIONS'])
def index():
	return json.dumps({'success': True, 'status': 'OK', 'message': 'Success'})

@clinic.route('/api/clinic/', methods=['PUT'])
def newClinic():
    data = request.data
    data  = data.decode('utf8').replace("'",'"')
    data = json.loads(data)
    print(data)
    success = False
    clinic = None
    message = ""

    success = ClinicService.createClinic(name=data['name'], address=data['address'])

    if success:
        message = "Clinic has been created."
        clinic = ClinicService.getClinicByData(data['name'], data['address'])
    else:
        message = "Clinic already exists."

    response = json.dumps({"success":success, "message":message, "clinic":clinic})
    return response

@clinic.route('/api/clinic/delete', methods=['DELETE'])
def deleteClinic():
    data = request.data
    data  = data.decode('utf8').replace("'",'"')
    data = json.loads(data)
    print(data)
    success = False
    clinic = None
    message = ""

    if ClinicService.clinicExistsById(data['id']):
        clinic = ClinicService.getClinicById(data['id'])
        success = ClinicService.deleteClinic(data['id'])
    if success:
        message= "Clinic deleted from the system."
    else:
        message= "Clinic cannot be deleted from the system."

    response = json.dumps({"success":success, "message":message, "clinic":clinic})
    return response

@clinic.route('/api/clinic/update', methods=['PUT'])
def updateClinic():
    data = request.data
    data = data.decode('utf8').replace("'", '"')
    data = json.loads(data)
    print(data)
    success = False
    clinic = None
    message = ""

    if ClinicService.clinicExistsById(data['id']):
        success = ClinicService.updateClinic(data['id'], data['name'], data['address'])
    if success:
        message = "Clinic has been updated."
        clinic = ClinicService.getClinicById(data['id'])
    else:
        message = "Clinic has not been updated."

    response = json.dumps(
        {"success": success, "message": message, "clinic": clinic})
    return response

# Returns all clinics
@clinic.route('/api/clinic/findAll', methods=['GET'])
def findAll():
    success = False
    message=""
    clinics = []

    clinics = ClinicService.getAllClinics()
    if clinics is not None:
        success = True
    else:
        success = False

    if success:
        message = "Clinic(s) retrieved."
    else:
        message = "No clinic(s) retrieved."

    response = json.dumps({"success":success, "message":message, "clinics":clinics})
    return response


@clinic.route('/api/clinic/find', methods=['POST'])
def findClinic():
    data = request.data
    data = data.decode('utf8').replace("'", '"')
    data = json.loads(data)
    print(data)
    success = False
    clinic = None
    message = ""
    
    clinic = ClinicService.getClinicById(data['clinic_id'])
    if clinic is not None:
        success = True
    else:
        success = False

    if success:
        message = "Clinic found."
    else:
        message = "No clinic found."

    response = json.dumps({"success":success, "message":message, "clinic":clinic})
    return response