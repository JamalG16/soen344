from index import db
from datetime import datetime
from datetime import time

# PickleType coverts python object to a string so that it can be stored on the database
class TimeSlot(db.Model):
    timeSlots = db.Column(db.PickleType, nullable=False, primary_key=True)
    
    def __iter__(self):
        yield 'timeSlots', self.timeSlots
        yield 'time', list(self.timeSlots.timeSlots.keys())
        yield 'available', list(self.timeSlots.timeSlots.values())

# Initializes the database
db.create_all()

#SLOTS = {time(8,00,00): False,time(8,20,00): False,time(8,40,00): False,time(9,0,00): False,time(9,20,00): False,time(9,40,00): False,time(10,00,00): False,time(10,20,00): False,time(10,40,00): False,time(11,00,00): False,time(11,20,00): False,time(11,40,00): False,time(12,00,00): False,time(12,20,00): False,time(12,40,00): False,time(13,00,00): False,time(13,20,00): False,time(13,40,00): False,time(14,00,00): False,time(14,20,00): False,time(14,40,00): False,time(15,00,00): False,time(15,20,00): False,time(15,40,00): False,time(16,00,00): False,time(16,20,00): False,time(16,40,00): False,time(17,00,00): False,time(17,20,00): False,time(17,40,00): False,time(18,00,00): False,time(18,20,00): False,time(18,40,00): False,time(19,00,00): False,time(19,20,00): False,time(19,40,00): False}
#SLOTS = ['8:00:00','8:20:00','8:40:00','9:00:00','9:20:00','9:40:00','10:00:00','10:20:00','10:40:00','11:00:00','11:20:00','11:40:00','12:00:00','12:20:00','12:40:00','13:00:00','13:20:00','13:40:00','14:00:00','14:20:00','14:40:00','15:00:00','15:20:00','15:40:00','16:00:00','16:20:00','16:40:00','17:00:00','17:20:00','17:40:00','18:00:00','18:20:00','18:40:00','19:00:00','19:20:00','19:40:00']
SLOTS = {'8:00:00': True,'8:20:00': True,'8:40:00': True,'9:00:00': True,'9:20:00': True,'9:40:00': True,'10:00:00': True,'10:20:00': True,'10:40:00': True,'11:00:00': True,'11:20:00': True,'11:40:00': True,'12:00:00': True,'12:20:00': True,'12:40:00': True,'13:00:00': True,'13:20:00': True,'13:40:00': True,'14:00:00': True,'14:20:00': True,'14:40:00': True,'15:00:00': True,'15:20:00': True,'15:40:00': True,'16:00:00': True,'16:20:00': True,'16:40:00': True,'17:00:00': True,'17:20:00': True,'17:40:00': True,'18:00:00': True,'18:20:00': True,'18:40:00': True,'19:00:00': True,'19:20:00': True,'19:40:00': True}

def createTimeSlots():
    newTimeSlots = TimeSlot(timeSlots=SLOTS)
    return newTimeSlots

def getTimeSlotAvail(time):
    return TimeSlot.query.filter_by(time = time).first().available

