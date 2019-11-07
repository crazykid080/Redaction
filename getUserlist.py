from flask import current_app
from main import app, User, db

with app.app_context():
	user = User()
	users = User.query.all()
	print(users)