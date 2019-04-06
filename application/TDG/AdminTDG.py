from application.models.Admin import Admin
from index import db


# Returns admin if found
def find(username):
    return Admin.query.filter_by(username=username).first()


def create(username, password_hash):
    newAdmin = Admin(username=username, password_hash=password_hash)
    # Add it to the database
    db.session.add(newAdmin)
    # Commit it
    db.session.commit()
