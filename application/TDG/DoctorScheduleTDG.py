from application.models.DoctorSchedule import DoctorSchedule
from index import db


# return all timeslots based on permit number, clinic and date
def find(permit_number, date, clinic_id=None):
    if clinic_id is None:
        return DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first()
    else:
        return DoctorSchedule.query.filter_by(permit_number=permit_number, date=date, clinic_id=clinic_id).first()

# create timeslots of a doctor on a specific date
def create(permit_number,timeSlots, date, clinic_id):
    newDoctorSchedule = DoctorSchedule(permit_number=permit_number, timeSlots=timeSlots, date=date, clinic_id=clinic_id)
    db.session.add(newDoctorSchedule)
    db.session.commit()

# update a doctor's timeslots on a specific date
def update(permit_number, date, timeSlots, clinic_id):
    schedule = DoctorSchedule.query.filter_by(permit_number=permit_number, date=date).first()
    schedule.timeSlots = timeSlots
    schedule.clinic_id = clinic_id
    db.session.commit()

# get schedules for all doctors except for one
def getAllSchedulesByDateExceptDoctor(date, permit_number, clinic_id=None):
    if clinic_id is None:
        return DoctorSchedule.query.filter(DoctorSchedule.permit_number != permit_number)\
                               .filter(DoctorSchedule.date == date).all()
    else:
        return DoctorSchedule.query.filter(DoctorSchedule.permit_number != permit_number) \
            .filter(DoctorSchedule.date == date).filter(DoctorSchedule.clinic_id == clinic_id).all()
