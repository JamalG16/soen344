from index import db

class Admin(db.Model):
	username = db.Column(db.String(30), primary_key=True)
	password_hash = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<admin %r>' % self.username

	# to iterate over an admin
	def __iter__(self):
		yield 'username', self.username
		yield 'password_hash', self.password_hash


# Initializes the database
db.create_all()



