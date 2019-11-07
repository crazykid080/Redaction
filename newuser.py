import sys
from getpass import getpass
from flask import current_app
from main import app, User, db
import flask_bcrypt as bcrypt
def main():
	"""Main entry point for script."""
	with app.app_context():
		print("Creating metadata")
		db.metadata.create_all(db.engine)
		print("done")
		print('Enter username: ')
		username = input()
		password = getpass()
		assert password == getpass('Password (again):')
		print("Enter clearance level")
		clearance = input()
		user = User(
			username=username, 
			password=bcrypt.generate_password_hash(password),
			clearance=clearance,
			role = "user")
		db.session.add(user)
		db.session.commit()
		print('User added.')


if __name__ == '__main__':
	main()