from index import db


class DoctorSchedule(db.Model):
    from application.models import Clinic
    permit_number = db.Column(db.String(), primary_key=True)
    date = db.Column(db.String(), primary_key=True)
    timeSlots = db.Column(db.String(), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)

    def __iter__(self):
        yield 'permit_number', self.permit_number
        yield 'date', self.date
        yield 'timeSlots', self.timeSlots
        yield 'clinic_id', self.clinic_id


# Initializes the database
db.create_all()
