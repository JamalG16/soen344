from application.TDG import RoomScheduleTDG
from application.services import RoomService
from application.util.Schedule import Schedule, Timeslot, ScheduleIterator

# Create an with all possible timeslots and whether it is available or not
SLOTS = '8:00:true,8:20:true,8:40:true,9:00:true,9:20:true,9:40:true,10:00:true,10:20:true,10:40:true,11:00:true,11:20:true,11:40:true,12:00:true,12:20:true,12:40:true,13:00:true,13:20:true,13:40:true,14:00:true,14:20:true,14:40:true,15:00:true,15:20:true,15:40:true,16:00:true,16:20:true,16:40:true,17:00:true,17:20:true,17:40:true,18:00:true,18:20:true,18:40:true,19:00:true,19:20:true,19:40:true'

def createTimeSlots(roomNumber, clinic_id, date):
    RoomScheduleTDG.create(roomNumber=roomNumber, clinic_id=clinic_id, timeSlots=SLOTS, date=date)
    return True

def getTimeSlotsByDateAndRoom(date, roomNumber, clinic_id):
    if RoomService.getRoom(roomNumber, clinic_id) is None:
        return None
    roomSchedule = RoomScheduleTDG.find(date=date, roomNumber=roomNumber, clinic_id=clinic_id)
    if roomSchedule is not None:
        return Schedule(roomSchedule.timeSlots)
    else:
        createTimeSlots(roomNumber=roomNumber, clinic_id=clinic_id, date=date)
        return Schedule(RoomScheduleTDG.find(roomNumber=roomNumber, clinic_id=clinic_id, date=date).timeSlots)

def getAllRoomNumbersByDate(date):
    listOfRoomSchedules = RoomScheduleTDG.find(date=date)
    listOfRoomNumbers = []
    if listOfRoomSchedules is None or len(listOfRoomSchedules) == 0:
        return []
    else:
        for room in listOfRoomSchedules:
            listOfRoomNumbers.append(room.roomNumber)
    return listOfRoomNumbers


# check if there is an available room at a specific time. If so, return the first room found to be available.
# Else, return None.
def findRoomAtTime(clinic_id, date, time):
	roomNumber = 'None'
	for room in RoomService.getAllRooms():
		if isRoomAvailable(roomNumber=room.roomNumber, clinic_id=clinic_id, date=date, time=time):
			roomNumber = room.roomNumber
			break
	return roomNumber

# Given a time, get a list that has all rooms available at the specified time.
# Then, check these rooms to find if a room is available for 3 consecutive time slots.
# Return a room, else return None.
def findRoomForAnnual(clinic_id, date, time):
	roomNumbers = []
	nextTimeSlot = None
	for room in RoomService.getAllRooms():
		if isRoomAvailable(roomNumber=room.roomNumber, clinic_id=clinic_id, date=date, time=time):
			roomNumbers.append(room.roomNumber)
	for roomNumber in roomNumbers:
		nextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=time).getTime()
		if nextTimeSlot is not None:
			if isRoomAvailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=nextTimeSlot):
				nextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=nextTimeSlot).getTime()
				if nextTimeSlot is not None:
					if isRoomAvailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=nextTimeSlot):
						return roomNumber
	return None

# Returns true if room's timeslot has been modified.
def toggleRoomTimeSlot(roomNumber, clinic_id, date, time):
	response = False
	room = RoomService.getRoom(roomNumber, clinic_id)
	if room is not None:
		if isRoomAvailable(roomNumber, clinic_id, date, time):
			makeTimeSlotUnavailable(roomNumber=roomNumber, date=date, time=time)
		else:
			makeTimeSlotAvailable(roomNumber=roomNumber, date=date, time=time)
		response = True
	return response

# Return true if slot is available, else return false.
def isRoomAvailable(roomNumber, clinic_id, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, clinic_id=clinic_id, date=date)
    if timeSlots is not None:
        return timeSlots.getTimeslots()[timeSlots.indexForTime(time)].isAvailable()
    else:
        return False

# Return the next time slot. If no next time slot, then return None.
def getNextTimeSlot(roomNumber, clinic_id, date, time):
    if time is '19:40':
        return None
    else:
        timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, clinic_id=clinic_id, date=date)
        iterator = timeSlots.getIterator()
        iterator.setAt(timeSlots.indexForTime(time)+1)
        if iterator.hasNext() is not None:
            return iterator.next()
        else:
            return None

# makes a timeslot available
def makeTimeSlotAvailable(roomNumber, clinic_id, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, clinic_id=clinic_id, date=date)
    index = timeSlots.indexForTime(time)
    timeSlots.getTimeslots()[index].setAvailable(True)
    timeSlots = timeSlots.toString()  # put back into db as a string
    RoomScheduleTDG.update(roomNumber=roomNumber, clinic_id=clinic_id, date=date, newTimeSlots=timeSlots)

# if the appointment is an annual, make all slots available
def makeTimeSlotAvailableAnnual(roomNumber, clinic_id, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextTimeSlot.getTime())

    makeTimeSlotAvailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=time)
    makeTimeSlotAvailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextTimeSlot.getTime())
    makeTimeSlotAvailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextNextTimeSlot.getTime())

#makes a timeslot unavailable
def makeTimeSlotUnavailable(roomNumber, clinic_id, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, clinic_id=clinic_id, date=date)
    index = timeSlots.indexForTime(time)
    timeSlots.getTimeslots()[index].setAvailable(False)
    timeSlots = timeSlots.toString()  # put back into db as a string
    RoomScheduleTDG.update(roomNumber=roomNumber, clinic_id=clinic_id, date=date, newTimeSlots=timeSlots)

# if the appointment is an annual, make all slots unavailable
def makeTimeSlotUnavailableAnnual(roomNumber, clinic_id, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextTimeSlot.getTime())

    makeTimeSlotUnavailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=time)
    makeTimeSlotUnavailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextTimeSlot.getTime())
    makeTimeSlotUnavailable(roomNumber=roomNumber, clinic_id=clinic_id, date=date, time=roomNextNextTimeSlot.getTime())
