from flask import current_app
from main import app, User, db

with app.app_context():
	user = User()
	users = User.query.all()
	print(users)
	print("Enter user to remove: ")
	userN = input()
	userD = User.query.filter_by(username=userN).first() 
	db.session.delete(userD)
	db.session.commit()