from application.TDG import RoomScheduleTDG
from application.services import RoomService

# Create an with all possible timeslots and whether it is available or not
SLOTS = '8:00:true,8:20:true,8:40:true,9:00:true,9:20:true,9:40:true,10:00:true,10:20:true,10:40:true,11:00:true,11:20:true,11:40:true,12:00:true,12:20:true,12:40:true,13:00:true,13:20:true,13:40:true,14:00:true,14:20:true,14:40:true,15:00:true,15:20:true,15:40:true,16:00:true,16:20:true,16:40:true,17:00:true,17:20:true,17:40:true,18:00:true,18:20:true,18:40:true,19:00:true,19:20:true,19:40:true'

# transform timeslots string into an array
def format(timeslots):
	return timeslots.split(",")

def createTimeSlots(roomNumber, date):
    RoomScheduleTDG.create(roomNumber=roomNumber, timeSlots=SLOTS, date=date)
    return True

def getTimeSlotsByDateAndRoom(date, roomNumber):
    if RoomService.getRoom(roomNumber) is None:
        return None
    roomSchedule = RoomScheduleTDG.find(date=date, roomNumber=roomNumber)
    if roomSchedule is not None:
        return format(roomSchedule.timeSlots)
    else:
        createTimeSlots(roomNumber=roomNumber, date=date)
        return format(RoomScheduleTDG.find(roomNumber=roomNumber, date=date).timeSlots)

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
def findRoomAtTime(date, time):
	roomNumber = 'None'
	for room in RoomService.getAllRooms():
		if isRoomAvailable(roomNumber=room.roomNumber, date=date, time=time):
			roomNumber = room.roomNumber
			break
	return roomNumber

# Given a time, get a list that has all rooms available at the specified time.
# Then, check these rooms to find if a room is available for 3 consecutive time slots.
# Return a room, else return None.
def findRoomForAnnual(date, time):
	roomNumbers = []
	nextTimeSlot = None
	for room in RoomService.getAllRooms():
		if isRoomAvailable(roomNumber=room.roomNumber, date=date, time=time):
			roomNumbers.append(room.roomNumber)
	for roomNumber in roomNumbers:
		nextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=time)
		if nextTimeSlot is not None:
			if isRoomAvailable(roomNumber=roomNumber, date=date, time=nextTimeSlot):
				nextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=nextTimeSlot)
				if nextTimeSlot is not None:
					if isRoomAvailable(roomNumber=roomNumber, date=date, time=nextTimeSlot):
						return roomNumber
	return None

# Returns true if room's timeslot has been modified.
def toggleRoomTimeSlot(roomNumber, date, time):
	response = False
	room = RoomService.getRoom(roomNumber)
	if room is not None:
		if isRoomAvailable(roomNumber, date, time):
			makeTimeSlotUnavailable(roomNumber=roomNumber, date=date, time=time)
		else:
			makeTimeSlotAvailable(roomNumber=roomNumber, date=date, time=time)
		response = True
	return response

# Return true if slot is available, else return false.
def isRoomAvailable(roomNumber, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, date=date)
    if timeSlots is not None:
        fulltime = time + ':true'
        return fulltime in timeSlots
    else:
        return False

# Return the next time slot. If no next time slot, then return None.
def getNextTimeSlot(roomNumber, date, time):
    if time is '19:40':
        return None
    else:
        timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, date=date)
        index = None
        if isRoomAvailable(roomNumber=roomNumber, date=date, time=time):
            index = timeSlots.index(time + ':true')
            return timeSlots[index+1][:-5] #increment the index to get next time slot
        else:
            index = timeSlots.index(time + ':false')
            return timeSlots[index+1][:-6] #increment the index to get next time slot

# makes a timeslot available
def makeTimeSlotAvailable(roomNumber, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, date=date)
    index = timeSlots.index(time + ':false')
    timeSlots[index] = time + ':true'
    timeSlots = ','.join(timeSlots)
    RoomScheduleTDG.update(roomNumber=roomNumber, date=date, newTimeSlots=timeSlots)

# if the appointment is an annual, make all slots available
def makeTimeSlotAvailableAnnual(roomNumber, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=roomNextTimeSlot)

    makeTimeSlotAvailable(roomNumber=roomNumber, date=date, time=time)
    makeTimeSlotAvailable(roomNumber=roomNumber, date=date, time=roomNextTimeSlot)
    makeTimeSlotAvailable(roomNumber=roomNumber, date=date, time=roomNextNextTimeSlot)

#makes a timeslot unavailable
def makeTimeSlotUnavailable(roomNumber, date, time):
    timeSlots = getTimeSlotsByDateAndRoom(roomNumber=roomNumber, date=date)
    index = timeSlots.index(time + ':true')
    timeSlots[index] = time + ':false'
    timeSlots = ','.join(timeSlots)
    RoomScheduleTDG.update(roomNumber=roomNumber, date=date, newTimeSlots=timeSlots)

# if the appointment is an annual, make all slots unavailable
def makeTimeSlotUnavailableAnnual(roomNumber, date, time):
    roomNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=time)
    roomNextNextTimeSlot = getNextTimeSlot(roomNumber=roomNumber, date=date, time=roomNextTimeSlot)

    makeTimeSlotUnavailable(roomNumber=roomNumber, date=date, time=time)
    makeTimeSlotUnavailable(roomNumber=roomNumber, date=date, time=roomNextTimeSlot)
    makeTimeSlotUnavailable(roomNumber=roomNumber, date=date, time=roomNextNextTimeSlot)
