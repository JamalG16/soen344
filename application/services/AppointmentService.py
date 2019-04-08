from application.services import RoomScheduleService, DoctorScheduleService
from application.services.PatientService import canBookAnnual, updateAnnual
from application.TDG import AppointmentTDG
from application.util import BooleanArrayOperations
import datetime


def createAppointment(room, clinic_id, doctor_permit_number, patient_hcnumber, length, time, date):
    dateSplit = date.split("-")
    date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
    AppointmentTDG.create(room=room, clinic_id=clinic_id, doctor_permit_number=doctor_permit_number,
                          patient_hcnumber=patient_hcnumber, length=length, time=time, date=date)
    return True


# find if a room is available and if a doctor is available to book an appointment.
# If so, book, the room and doctor at the specified time, with the specified patient, for a type of appointment.
# If the type is to be annual, the patient's last annual must be checked to validate the new annual (at least 1 year difference).
# Also, if the type is annual, check that the next two time slots can be booked in the same room with the same doctor.
def bookAppointment(patient_hcnumber, length, time, date, clinic_id):
    if length == '20':  # checkup
        available_doctor = DoctorScheduleService.findDoctorAtTime(date, time, clinic_id=clinic_id)
        available_room = RoomScheduleService.findRoomAtTime(time=time, date=date, clinic_id=clinic_id)
        if available_doctor is None or available_room is None:
            return False
        return bookRegular(patient_hcnumber=patient_hcnumber, doctor_permit_number=available_doctor,
                           room_number=available_room, length=length, time=time, date=date, clinic_id=clinic_id)
    elif length == '60':  # annual
        if not canBookAnnual(patient_hcnumber):
            return False
        available_doctor = DoctorScheduleService.findDoctorForAnnual(date, time)
        available_room = RoomScheduleService.findRoomForAnnual(clinic_id, date, time)
        if available_doctor is None | available_room is None:
            return False
        return bookAnnual(patient_hcnumber=patient_hcnumber, doctor_permit_number=available_doctor,
                          room_number=available_room, length=length, time=time, date=date, clinic_id=clinic_id)
    else:
        return False


def bookAppointmentWithASpecificDoctor(patient_hcnumber, doctor_permit_number, length, time, date, clinic_id):
    if length == 20:  # checkup
        available_doctor = doctor_permit_number
        available_room = RoomScheduleService.findRoomAtTime(time=time, date=date, clinic_id=clinic_id)
        if available_room is None:
            return False
        return bookRegular(patient_hcnumber=patient_hcnumber, doctor_permit_number=available_doctor,
                           room_number=available_room, length=length, time=time, date=date, clinic_id=clinic_id)
    elif length == 60:  # annual
        if not canBookAnnual(patient_hcnumber):
            return False
        available_doctor = doctor_permit_number
        available_room = RoomScheduleService.findRoomForAnnual(clinic_id, date, time)
        if available_room is None:
            return False
        return bookAnnual(patient_hcnumber=patient_hcnumber, doctor_permit_number=available_doctor,
                          room_number=available_room, length=length, time=time, date=date, clinic_id=clinic_id)
    else:
        return False


def bookRegular(patient_hcnumber, doctor_permit_number, room_number, clinic_id, length, time, date):
    DoctorScheduleService.makeTimeSlotUnavailable(doctor_permit_number, date, time)
    RoomScheduleService.makeTimeSlotUnavailable(roomNumber=room_number, date=date, time=time, clinic_id=clinic_id)
    createAppointment(room=room_number, doctor_permit_number=doctor_permit_number, patient_hcnumber=patient_hcnumber,
                      length=length, time=time, date=date, clinic_id=clinic_id)
    return True


def bookAnnual(patient_hcnumber, doctor_permit_number, room_number, clinic_id, length, time, date):
    DoctorScheduleService.makeTimeSlotUnavailableAnnual(doctor_permit_number, date, time)
    RoomScheduleService.makeTimeSlotUnavailableAnnual(roomNumber=room_number, date=date, time=time, clinic_id=clinic_id)
    if createAppointment(room=room_number, doctor_permit_number=doctor_permit_number, patient_hcnumber=patient_hcnumber,
                         length=length, time=time, date=date, clinic_id=clinic_id):
        updateAnnual(patient_hcnumber, date)
    return True


def is_patient_already_booked(patient_hcnumber, time, date, length, clinic_id):
    for appointment in getAppointments(patient_hcnumber=patient_hcnumber):
        if appointment['time'] == time \
                and appointment['date'] == date \
                and appointment['length'] == length \
                and appointment['clinic_id'] == clinic_id:
            return True
    return False


# gets the appointment based on id
def getAppointment(id):
    appointment = AppointmentTDG.find(id)
    if appointment is None:
        return None
    else:
        return dict(appointment)


# gets all patient's appointments. Returns an array, where each value contains an appointment in the form of a dict.
def getAppointments(patient_hcnumber):
    apps = []
    appointments = AppointmentTDG.findAll(patient_hcnumber=patient_hcnumber)
    for appointment in appointments:
        apps.append(dict(appointment))
    return apps


# gets all appointments for this doctor in an array
def getDoctorAppointments(doctor_permit_number):
    apps = []
    appointments = AppointmentTDG.findForDoctor(doctor_permit_number=doctor_permit_number)
    for appointment in appointments:
        apps.append(dict(appointment))
    return apps


# cancels an appointment and frees the time slots
def cancelAppointment(id):
    appointment = getAppointment(id)
    if appointment is None:
        return False
    else:
        doctor = appointment['doctor_permit_number']
        room = appointment['room']
        date = appointment['date']
        time = appointment['time']
        clinic_id = appointment['clinic_id']
        if appointment['length'] == 20:
            DoctorScheduleService.makeTimeSlotAvailable(doctor, date, time)
            RoomScheduleService.makeTimeSlotAvailable(roomNumber=room, date=date, time=time, clinic_id=clinic_id)
            AppointmentTDG.delete(appointment['id'])
            return True
        elif appointment['length'] == 60:
            DoctorScheduleService.makeTimeSlotAvailableAnnual(doctor, date, time)
            RoomScheduleService.makeTimeSlotAvailable(roomNumber=room, date=date, time=time, clinic_id=clinic_id)
            updateAnnual(appointment['patient_hcnumber'], None)
            AppointmentTDG.delete(appointment['id'])
            return True
        else:
            return False


# updates the information of an appointment

def updateDB(id, clinic_id, room, doctor_permit_number, length, time, date):
    dateSplit = date.split("-")
    date = datetime.datetime.strptime(dateSplit[0] + dateSplit[1] + dateSplit[2], '%Y%m%d').date()
    AppointmentTDG.update(id=id, clinic_id=clinic_id, room=room, doctor_permit_number=doctor_permit_number,
                          length=length, time=time, date=date)


# gets the currently made appointment and tries to change it to the new appointment parameters.
# 4 cases: 20mins --> 20mins, 20mins-->60mins, 60mins-->20mins, 60mins-->60mins
def updateAppointment(appointment_id, doctor_permit_number, length, new_time, new_date):
    old_appointment = getAppointment(appointment_id)
    old_appointment_is_annual = old_appointment['length'] == 60
    new_appointment_is_annual = length == 60
    appointment_updated = False
    if new_appointment_is_annual and not old_appointment_is_annual \
            and canBookAnnual(old_appointment['patient_hcnumber']):
        return "Patient already has an annual appointment which is not the one being moved", appointment_updated

    if doctor_permit_number is None:
        appointment_updated = bookAppointment(patient_hcnumber=old_appointment['patient_hcnumber'],
                                              length=length, time=new_time, date=new_date,
                                              clinic_id=old_appointment['clinic_id'])
    else:
        appointment_updated = bookAppointmentWithASpecificDoctor(patient_hcnumber=old_appointment['patient_hcnumber'],
                                                                 doctor_permit_number=doctor_permit_number,
                                                                 length=length, time=new_time, date=new_date,
                                                                 clinic_id=old_appointment['clinic_id'])
    cancelAppointment(appointment_id)

    message = "Appointment has been updated" if appointment_updated else "Appointment was not updated"

    return message, appointment_updated


def crossCheckDoctorAndRoomList(date, doctorPermitNumberList, roomList, clinic_id):
    available_time_slots = [False] * 36
    # preferential filtering by doctors, since they are the ones to most likely have fewer availabilities
    for permit_number in doctorPermitNumberList:
        doctor_time_slots = DoctorScheduleService.getTimeSlotsByDateAndDoctor(permit_number=permit_number,
                                                                              date=date).toString().split(',')
        # for all available rooms
        # concatenate existing availabilities with the cross availabilities of each room and the doc schedule
        for roomNumber in roomList:
            room_slots = RoomScheduleService.getTimeSlotsByDateAndRoom(date=date, roomNumber=roomNumber,
                                                                       clinic_id=clinic_id).toString().split(',')
            common_time_slots = BooleanArrayOperations.getCommonTimeslots(doctor_time_slots, room_slots)
            available_time_slots = BooleanArrayOperations.concatenateBooleanLists(available_time_slots,
                                                                                  common_time_slots)
    return available_time_slots
