from application.TDG import DoctorScheduleTDG
from application.services.DoctorService import getAllDoctors, getDoctor, getAllDoctorPermits
from application.services.AppointmentService import getDoctorAppointments
from application.util.Schedule import Schedule, Timeslot, ScheduleIterator

# Create an with all possible timeslots and unavailable by default
SLOTS = '8:00:false,8:20:false,8:40:false,9:00:false,9:20:false,9:40:false,10:00:false,10:20:false,10:40:false,' \
        '11:00:false,11:20:false,11:40:false,12:00:false,12:20:false,12:40:false,13:00:false,13:20:false,13:40:false,' \
        '14:00:false,14:20:false,14:40:false,15:00:false,15:20:false,15:40:false,16:00:false,16:20:false,16:40:false,' \
        '17:00:false,17:20:false,17:40:false,18:00:false,18:20:false,18:40:false,19:00:false,19:20:false,19:40:false'


def createTimeSlots(permit_number, date):
    DoctorScheduleTDG.create(permit_number=permit_number, timeSlots=SLOTS, date=date)
    return True


def getTimeSlotsByDateAndDoctor(permit_number, date):
    doctorSchedule = DoctorScheduleTDG.find(permit_number=permit_number, date=date)
    if doctorSchedule is not None:
        return Schedule(doctorSchedule.timeSlots)
    else:
        return None


def getAllAvailableDoctorPermitsByDate(date):
    all_doctors_permit_numbers = getAllDoctorPermits()
    available_doctors_permit_numbers = []
    for permit in all_doctors_permit_numbers:
        doctor_availability = DoctorScheduleTDG.find(permit_number=permit,date=date)
        if doctor_availability is not None:
            available_doctors_permit_numbers.append(doctor_availability.permit_number)
    return available_doctors_permit_numbers


# Return true if slot is available, else return false.
def isDoctorAvailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    if timeSlots is not None:
        return timeSlots.getTimeslots()[timeSlots.indexForTime(time)].isAvailable()
    else:
        return None


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
            if nextTimeSlot.isAvailable():
                nextTimeSlot = getNextTimeSlot(permit_number, date, nextTimeSlot.getTime())
                if nextTimeSlot is not None:
                    if nextTimeSlot.isAvailable():
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
        iterator = timeSlots.getIterator()
        iterator.setAt(timeSlots.indexForTime(time)+1)
        if iterator.hasNext() is not None:
            return iterator.next()
        else:
            return None


# makes a specific timeslot available
def makeTimeSlotAvailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    index = timeSlots.indexForTime(time)
    timeSlots.getTimeslots()[index].setAvailable(True)
    timeSlots = timeSlots.toString()  # put back into db as a string
    DoctorScheduleTDG.update(permit_number=permit_number, date=date, timeSlots=timeSlots)

# if the appointment is an annual, make all necessary slots available
def makeTimeSlotAvailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot.getTime())

    makeTimeSlotAvailable(permit_number, date, time)
    makeTimeSlotAvailable(permit_number, date, doctorNextTimeSlot.getTime())
    makeTimeSlotAvailable(permit_number, date, doctorNextNextTimeSlot.getTime())

#makes a specific timeslot unavailable
def makeTimeSlotUnavailable(permit_number, date, time):
    timeSlots = getTimeSlotsByDateAndDoctor(permit_number, date)
    index = timeSlots.indexForTime(time)
    timeSlots.getTimeslots()[index].setAvailable(False)
    timeSlots = timeSlots.toString()  # put back into db as a string
    DoctorScheduleTDG.update(permit_number=permit_number, date=date, timeSlots=timeSlots)

# if the appointment is an annual, make all necessary slots unavailable
def makeTimeSlotUnavailableAnnual(permit_number, date, time):
    doctorNextTimeSlot = getNextTimeSlot(permit_number, date, time)
    doctorNextNextTimeSlot = getNextTimeSlot(permit_number, date, doctorNextTimeSlot.getTime())

    makeTimeSlotUnavailable(permit_number, date, time)
    makeTimeSlotUnavailable(permit_number, date, doctorNextTimeSlot.getTime())
    makeTimeSlotUnavailable(permit_number, date, doctorNextNextTimeSlot.getTime())


# Given an array of timeslots, a date and a permit number, create schedules for time slots in the date.
def setAvailability(permit_number, date, timeslots):
    schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)
    return_value = {}
    # should not happend
    if schedule_timeslots is None:
        createTimeSlots(permit_number, date)
        schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)
    else:  # verify that if a doctor wants to make himself available during an already made appointment he can't
        doctor_appointment = getDoctorAppointments(permit_number)
        new_schedule = createFromBooleanArray(timeslots)
        for appointment in doctor_appointment:
            if appointment['date'] == date:
                for index in range(0, appointment['length'], 20):
                    minutes = int(appointment['time'][len(appointment['time']) - 2:]) + index
                    hours = int(appointment['time'][:len(appointment['time']) - 3])
                    if minutes >= 60:
                        hours += 1
                        minutes -= 60

                    if minutes == 0:
                        minutes = '00'
                    else:
                        minutes = str(minutes)
                    hours = str(hours)
                    if new_schedule.getTimeslots()[new_schedule.indexForTime(hours + ':' + minutes)].isAvailable():
                        return_value['success'] = False
                        return_value['message'] = "Availability Not Modified, one or more timeslot to be made " \
                                                  "available was in conflict with an existing appointment."
                        return return_value

    doctors_schedule = DoctorScheduleTDG.getAllSchedulesByDateExceptDoctor(date, permit_number)
    timeslot_iterator = schedule_timeslots.getIterator()
    new_timeslot_iterator = createFromBooleanArray(timeslots).getIterator()
    i = 0
    while new_timeslot_iterator.hasNext() and timeslot_iterator.hasNext():
        new_value = new_timeslot_iterator.next()
        old_value = timeslot_iterator.next()
        if new_value.isAvailable():
            # if doctor wants to be available check that 7 doctors are not available at that time
            number_of_doctor = 0
            for schedule in doctors_schedule:
                schedule = Schedule(schedule)
                if schedule.getTimeslots()[i].isAvailable():
                    number_of_doctor = number_of_doctor + 1

            if number_of_doctor >= 7:
                return_value['success'] = False
                return_value['message'] = "Availability Not Modified, conflict in schedule with 7 doctors " \
                                          "or more."
                return return_value

            old_value.setAvailable(True)
        else:
            old_value.setAvailable(False)
        i = i+1

    DoctorScheduleTDG.update(permit_number, date, schedule_timeslots.toString())
    return_value['success'] = True
    return_value['message'] = "Availability Modified."
    return return_value


# Given a date and a permit number, create schedules for time slots in the date.
def getAvailability(permit_number, date):
    schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)
    if schedule_timeslots is None:
        createTimeSlots(permit_number, date)
        schedule_timeslots = getTimeSlotsByDateAndDoctor(permit_number, date)

    return schedule_timeslots.toString().split(',')

def createFromBooleanArray(array):
    schedule = Schedule(SLOTS)
    schedule_iterator = schedule.getIterator()
    index = 0
    while schedule_iterator.hasNext():
        timeslot = schedule_iterator.next()
        timeslot.setAvailable(array[index])
        index += 1
    return schedule


def createBooleanArray(schedule):
    schedule_iterator = schedule.getIterator()
    index = 0
    array = []
    while schedule_iterator.hasNext():
        timeslot = schedule_iterator.next()
        array.append(timeslot.isAvailable())
        index += 1
    return array
