from application.models.DoctorSchedule import DoctorSchedule
from index import db

# return all timeslots based on permit number and date
def find(permit_number, date):
    return DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first()
    
# create timeslots of a doctor on a specific date
def create(permit_number,timeSlots, date):
    newDoctorSchedule = DoctorSchedule(permit_number=permit_number, timeSlots=timeSlots, date=date)
    db.session.add(newDoctorSchedule)
    db.session.commit()

# update a doctor's timeslots on a specific date
def update(permit_number, date, timeSlots):
    DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first().timeSlots = timeSlots
    db.session.commit()
