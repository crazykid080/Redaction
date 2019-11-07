from flask import current_app
from main import app, User, db

with app.app_context():
	users = User.query.all()
	print(users)
	print("Enter user to authorize: ")
	userN = input()
	user = User.query.filter_by(username=userN).first() 
	user.role = 'admin'
	db.session.commit()