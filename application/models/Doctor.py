from index import db
from passlib.hash import sha256_crypt


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
