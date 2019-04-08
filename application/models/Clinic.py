from index import db

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False, unique=True)

    def __iter__(self):
        yield 'id', self.id
        yield 'clinic_id', self.clinic_id
        yield 'name', self.name
        yield 'address', self.address

# Initializes the database
db.create_all()
