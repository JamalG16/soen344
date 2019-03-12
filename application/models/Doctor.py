from index import db
from datetime import datetime
from passlib.hash import sha256_crypt
from .DoctorSchedule import getTimeSlotsByDateAndDoctor, makeTimeSlotAvailable, makeTimeSlotUnavailable, getNextTimeSlot

class Doctor(db.Model):
    permit_number = db.Column(db.String(7), nullable=False, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    specialty = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Doctor %r %r>' % self.fname % self.lname

    # to iterate over a patient to retrieve specific attributes
    def __iter__(self):
        yield 'permit_number', self.permit_number
        yield 'fname', self.fname
        yield 'lname', self.lname
        yield 'specialty', self.specialty
        yield 'password_hash', self.password_hash
        yield 'city', self.city

# Initializes the database
db.create_all()


# Returns True if doctor exists
def doctorExists(permit_number):
    return Doctor.query.filter_by(permit_number=permit_number).first() is not None


# Returns true if doctor is authenticated
def authenticate(permit_number, password):
    verified = False
    user = getDoctor(permit_number)
    if user is not None:
        verified = sha256_crypt.verify(password, user['password_hash'])

    return verified


# Returns true if password hash is the right one
def verifyHash(permit_number, password_hash):
    verified = False
    user = getDoctor(permit_number)
    if user is not None:
        verified = (password_hash == user['password_hash'])

    return verified


# Returns Doctor if found
def getDoctor(permit_number):
    doctor = Doctor.query.filter_by(permit_number=permit_number).first()
    if doctor is None:
        return None
    else:
        return dict(doctor)


# Returns True if doctor is created
def createDoctor(permit_number, fname, lname, specialty, password, city):
    reponse = False
    if doctorExists(permit_number):
        reponse =  False # if doctor exists then return false
    else:
        # hash password
        password_hash = sha256_crypt.hash(password)

        # Create the new doctor
        newDoctor = Doctor(permit_number=permit_number, fname=fname, lname=lname, password_hash=password_hash, specialty=specialty, city=city)

        # Add it to the database
        db.session.add(newDoctor)

        # Commit it
        db.session.commit()

        reponse = True
    return reponse


# check if doctor is available at a specific time
def doctorAvailable(permit_number, time):
    if doctorExists(permit_number):
        doctorTimeSlots = format(getTimeSlotsByDateAndDoctor(permit_number, datetime(2009, 5, 5)))
        time = time + ':true'
        return time in doctorTimeSlots
    else:
        return False


# check if there is an available doctor at a specific time. If so, return the first doctor found to be available.
# Else, return None.
def findDoctorAtTime(time):
    permit_number = None
    for doctor in db.session.query(Doctor.permit_number).all():
        if doctorAvailable(doctor.permit_number, time):
            permit_number = doctor.permit_number
            break
    return permit_number


# Returns true if doctor's timeslot has been modified.
def toggleDoctorTimeSlot(permit_number, time):
    response = False
    doctor = getDoctor(permit_number)
    if doctor is not None:
        if doctorAvailable(permit_number, time):
            makeTimeSlotUnavailable(permit_number, time)
        else:
            makeTimeSlotAvailable(permit_number, time)
        response = True
    return response


# Given a time, get a list that has all doctors available at the specified time.
# Then, check these doctors to find if a doctor is available for 3 consecutive time slots.
# Return a doctor, else return None.
def findDoctorForAnnual(time):
    permit_numbers = []
    nextTimeSlot = None
    for doctor in db.session.query(Doctor.permit_number).all():
        if doctorAvailable(doctor.permit_number, time):
            permit_numbers.append(doctor.permit_number)
    for permit_number in permit_numbers:
        nextTimeSlot = getNextTimeSlot(permit_number, time)
        if nextTimeSlot is not None:
            if doctorAvailable(permit_number, nextTimeSlot):
                nextTimeSlot = getNextTimeSlot(permit_number, nextTimeSlot)
                if nextTimeSlot is not None:
                    if doctorAvailable(permit_number, nextTimeSlot):
                        return permit_number
    return None

