from index import db
from .Doctor import *
from datetime import datetime
from datetime import time
import json

# PickleType coverts python object to a string so that it can be stored on the database
class DoctorSchedule(db.Model):
    permit_number = db.Column(db.String(), nullable=False, primary_key=True)
    date = db.Column(db.String(), nullable=False, primary_key=True)
    timeSlots = db.Column(db.String(), nullable=False)

    def __iter__(self):
        yield 'permit_number', self.permit_number
        yield 'date', self.date
        yield 'timeSlots', self.timeSlots

# Create an with all possible timeslots and unavailable by default
SLOTS = '8:00:false,8:20:false,8:40:false,9:00:false,9:20:false,9:40:false,10:00:false,10:20:false,10:40:false,11:00:false,11:20:false,11:40:false,12:00:false,12:20:false,12:40:false,13:00:false,13:20:false,13:40:false,14:00:false,14:20:false,14:40:false,15:00:false,15:20:false,15:40:false,16:00:false,16:20:false,16:40:false,17:00:false,17:20:false,17:40:false,18:00:false,18:20:false,18:40:false,19:00:false,19:20:false,19:40:false'

def createTimeSlots(permit_number, date):
    newDoctorSchedule = DoctorSchedule(permit_number=permit_number, timeSlots=SLOTS, date=date)
    db.session.add(newDoctorSchedule)
    db.session.commit()
    return newDoctorSchedule

def getAllTimeSlotsByDoctor(permit_number):
    return format(DoctorSchedule.query.filter_by(permit_number=permit_number).timeSlots)

def getAllTimeSlotsByDate(date):
    return format(DoctorSchedule.query.filter_by(date=date).timeSlots)

def getTimeSlotsByDateAndDoctor(permit_number, date):
    return format(DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first().timeSlots)

# check if there is an available doctor at a specific time. If so, return the first doctor found to be available.
# Else, return None.
def findDoctorAtTime(date, time):
    permit_number = None
    for doctor in getAllDoctors():
        if isDoctorAvailable(doctor.permit_number, date, time):
            permit_number = doctor.permit_number
            break
    return permit_number

# Given a time, get a list that has all doctors available at the specified time.
# Then, check these doctors to find if a doctor is available for 3 consecutive time slots.
# Return a doctor, else return None.
def findDoctorForAnnual(date, time):
	permit_numbers = []
	nextTimeSlot = None
	for doctor in getAllDoctors():
		if isDoctorAvailable(doctor.permit_number, date, time):
			permit_numbers.append(doctor.permit_number)
	for permit_number in permit_numbers:
		nextTimeSlot = getNextTimeSlot(permit_number, date, time)
		if nextTimeSlot is not None:
			if isDoctorAvailable(permit_number, date, nextTimeSlot):
				nextTimeSlot = getNextTimeSlot(permit_number, date, nextTimeSlot)
				if nextTimeSlot is not None:
					if isDoctorAvailable(permit_number, date, nextTimeSlot):
						return permit_number
	return None

# Returns true if doctor's timeslot has been modified.
def toggleDoctorTimeSlot(permit_number, date, time):
	response = False
	doctor = getDoctor(permit_number)
	if doctor is not None:
		if isDoctorAvailable(permit_number, date, time):
			makeTimeSlotUnavailable(permit_number, date, time)
		else:
			makeTimeSlotAvailable(permit_number, date, time)
		response = True
	return response

# transform timeslots string into an array
def format(timeSlots):
	return timeSlots.split(",")

# Return true if slot is available, else return false.
def isDoctorAvailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    fulltime = time + ':true'
    return fulltime in timeSlots

# Return the next time slot. If no next time slot, then return None.
def getNextTimeSlot(permit_number, date, time):
    if time is '19:40':
        return None
    else:
        timeSlots = format(getAllTimeSlotsByDoctor(permit_number))
        index = None
        if isDoctorAvailable(permit_number, date, time):
            index = timeSlots.index(time + ':true')
            return timeSlots[index+1][:-5] #increment the index to get next time slot
        else:
            index = timeSlots.index(time + ':false')
            return timeSlots[index+1][:-6] #increment the index to get next time slot


# makes a specific timeslot available
def makeTimeSlotAvailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    index = timeSlots.index(time + ':false')
    timeSlots[index] = time + ':true'
    DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first().timeSlots = ','.join(timeSlots) # put back into db as a string
    db.session.commit()

# if the appointment is an annual, make all necessary slots available
def makeTimeSlotAvailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot)

    makeTimeSlotAvailable(permit_number, date, time)
    makeTimeSlotAvailable(permit_number, date, doctorNextTimeSlot)
    makeTimeSlotAvailable(permit_number, date, doctorNextNextTimeSlot)
    db.session.commit()

#makes a specific timeslot unavailable
def makeTimeSlotUnavailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    index = timeSlots.index(time + ':true')
    timeSlots[index] = time + ':false'
    DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first().timeSlots = ','.join(timeSlots) #put back into db as a string
    db.session.commit()

# if the appointment is an annual, make all necessary slots unavailable
def makeTimeSlotUnavailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot)

    makeTimeSlotUnavailable(permit_number, date, time)
    makeTimeSlotUnavailable(permit_number, date, doctorNextTimeSlot)
    makeTimeSlotUnavailable(permit_number, date, doctorNextNextTimeSlot)
    db.session.commit()
