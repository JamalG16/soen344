from application.TDG import DoctorScheduleTDG
from application.services.DoctorService import getAllDoctors, getDoctor, getAllDoctorPermits

# Create an with all possible timeslots and unavailable by default
SLOTS = '8:00:false,8:20:false,8:40:false,9:00:false,9:20:false,9:40:false,10:00:false,10:20:false,10:40:false,11:00:false,11:20:false,11:40:false,12:00:false,12:20:false,12:40:false,13:00:false,13:20:false,13:40:false,14:00:false,14:20:false,14:40:false,15:00:false,15:20:false,15:40:false,16:00:false,16:20:false,16:40:false,17:00:false,17:20:false,17:40:false,18:00:false,18:20:false,18:40:false,19:00:false,19:20:false,19:40:false'

# transform timeslots string into an array
def format(timeSlots):
	return timeSlots.split(",")

def createTimeSlots(permit_number, date):
    DoctorScheduleTDG.create(permit_number=permit_number, timeSlots=SLOTS, date=date)
    return True

def getTimeSlotsByDateAndDoctor(permit_number, date):
    doctorSchedule = DoctorScheduleTDG.find(permit_number=permit_number, date=date)
    if doctorSchedule is not None:
        return format(doctorSchedule.timeSlots)
    else:
        return None

def getAllAvailableDoctorPermitsByDate(date):
    all_doctors_permit_numbers = getAllDoctorPermits()
    available_doctors_permit_numbers=[]
    for permit in all_doctors_permit_numbers:
        doctor_availability = DoctorScheduleTDG.find(permit_number=permit,date=date)
        if doctor_availability is not None:
            available_doctors_permit_numbers.append(doctor_availability.permit_number)
    return available_doctors_permit_numbers


# Return true if slot is available, else return false.
def isDoctorAvailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    if timeSlots is not None:
        fulltime = time + ':true'
        return fulltime in timeSlots
    else:
        return None

def isDoctorAvailableForAnnual(permit_number,date,time):
    count=0
    while isDoctorAvailable(permit_number,date,time) & count<3 :
        time = getNextTimeSlot(permit_number,date,time)
        count+=1
    # 3 subesequent slots are available from the initial time
    return count==3

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

# Return the next time slot. If no next time slot, then return None.
def getNextTimeSlot(permit_number, date, time):
    if time is '19:40':
        return None
    else:
        timeSlots = getTimeSlotsByDateAndDoctor(permit_number=permit_number, date=date)
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
    timeSlots = ','.join(timeSlots) # put back into db as a string
    DoctorScheduleTDG.update(permit_number=permit_number, date=date, timeSlots=timeSlots)

# if the appointment is an annual, make all necessary slots available
def makeTimeSlotAvailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot)

    makeTimeSlotAvailable(permit_number, date, time)
    makeTimeSlotAvailable(permit_number, date, doctorNextTimeSlot)
    makeTimeSlotAvailable(permit_number, date, doctorNextNextTimeSlot)

#makes a specific timeslot unavailable
def makeTimeSlotUnavailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    index = timeSlots.index(time + ':true')
    timeSlots[index] = time + ':false'
    timeSlots = ','.join(timeSlots) # put back into db as a string
    DoctorScheduleTDG.update(permit_number=permit_number, date=date, timeSlots=timeSlots)

# if the appointment is an annual, make all necessary slots unavailable
def makeTimeSlotUnavailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot)

    makeTimeSlotUnavailable(permit_number, date, time)
    makeTimeSlotUnavailable(permit_number, date, doctorNextTimeSlot)
    makeTimeSlotUnavailable(permit_number, date, doctorNextNextTimeSlot)


# Given an array of timeslots, a date and a permit number, create schedules for time slots in the date.
def setAvailability(permit_number, date, timeslots):
    schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)
    # should not happend
    if schedule_timeslots is None:
        createTimeSlots(permit_number, date)
        schedule_timeslots = format(DoctorScheduleTDG.find(permit_number, date).timeSlots)

    doctors_schedule = DoctorScheduleTDG.getAllSchedulesByDateExceptDoctor(date, permit_number)
    i = 0
    for new_value in timeslots:
        if new_value:
            # if doctor wants to be available check that 7 doctors are not available at that time
            number_of_doctor = 0
            for schedule in doctors_schedule:
                if getBooleanValue(format(schedule.timeSlots)[i]):
                    number_of_doctor = number_of_doctor + 1

            if number_of_doctor >= 7:
                return False

            schedule_timeslots[i] = getTimeValue(schedule_timeslots[i]) + 'true'
        else:
            schedule_timeslots[i] = getTimeValue(schedule_timeslots[i]) + 'false'
        i = i+1

    DoctorScheduleTDG.update(permit_number, date, ','.join(schedule_timeslots))
    return True


# Given an array of timeslots, a date and a permit number, create schedules for time slots in the date.
def getAvailability(permit_number, date):
    schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)
    if schedule_timeslots is None:
        createTimeSlots(permit_number, date)
        schedule_timeslots = format(DoctorScheduleTDG.find(permit_number, date).timeSlots)

    return schedule_timeslots


def getTimeValue(timeslot):
    index = 0
    if timeslot.find('t') is not -1:
        index = timeslot.index('t')
    else:
        index = timeslot.index('f')

    return timeslot[:index]


def getBooleanValue(timeslot):
    index = 0
    if timeslot.find('t') is not -1:
        index = timeslot.index('t')
    else:
        index = timeslot.index('f')

    return timeslot[index:]
