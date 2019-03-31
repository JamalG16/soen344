import abc


class Iterable(abc.ABC):
    @abc.abstractmethod
    def getIterator(self):
        pass


class Iterator(abc.ABC):
    @abc.abstractmethod
    def hasNext(self):
        pass

    @abc.abstractmethod
    def next(self):
        pass

    @abc.abstractmethod
    def setAt(self, index):
        pass


class ScheduleIterator(Iterator):

    def __init__(self, schedule):
        if not isinstance(schedule, Schedule):
            raise Exception('Invalid parameters, Schedule iterator needs instance of Schedule class')
        self.schedule = schedule.getTimeslots()
        self.currentIndex = 0

    def hasNext(self):
        return self.currentIndex < len(self.schedule) - 1

    def next(self):
        if self.currentIndex == len(self.schedule):
            return None
        self.currentIndex += 1
        return self.schedule[self.currentIndex-1]

    def setAt(self, index):
        if index < 0 or index >= len(self.schedule):
            self.currentIndex = len(self.schedule)-1
        else:
            self.currentIndex = index


class Schedule(Iterable):

    def __init__(self, timeslots):
        self.timeslots = formatTimeSlots(timeslots)

    def getIterator(self):
        return ScheduleIterator(self)

    def getTimeslots(self):
        return self.timeslots

    # given an array of timeslot, return a string
    def toString(self):
        string = ""
        for timeslot in self.timeslots:
            string += timeslot.toString() + ","

        return string[:len(string)-1]

    def indexForTime(self, time):
        for timeslot in self.timeslots:
            if timeslot.getTime() == time:
                return self.timeslots.index(timeslot)
        return None


class Timeslot:

    def __init__(self, time, available):
        self.time = time
        self.available = (available == "true")

    def toString(self):
        if self.isAvailable():
            boolean_value = "true"
        else:
            boolean_value = "false"
        return self.time + ":" + boolean_value

    def getTime(self):
        return self.time

    def isAvailable(self):
        return self.available

    def setAvailable(self, available):
        self.available = available


# transform timeslots string into an array
def formatTimeSlots(timeSlots):
    arrayTime = timeSlots.split(",")
    arrayTimeslots = []
    for timeslot in arrayTime:
        arrayTimeslots.append(Timeslot(getTimeValue(timeslot), getBooleanValue(timeslot)))

    return arrayTimeslots


def getTimeValue(timeslot):
    if timeslot.find('t') is not -1:
        index = timeslot.index('t')
    else:
        index = timeslot.index('f')

    return timeslot[:index-1]


def getBooleanValue(timeslot):
    if timeslot.find('t') is not -1:
        index = timeslot.index('t')
    else:
        index = timeslot.index('f')

    return timeslot[index:]
