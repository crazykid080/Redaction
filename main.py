import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import flask_bcrypt as bcrypt

class LoginForm(FlaskForm):
	username = StringField('Username')
	password = PasswordField('Password')
	submit = SubmitField('Login')
	
app = Flask(__name__)
db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.init_app(app)
app.config['SECRET_KEY'] = b'u\xe0\xce\xce\xb7\xfb\xea?\x80\xf4\x9c(\xbc\n\xd9\xb0qi\x87\xa9t/B\x9b\x82/fS\x07\x08!\xb7\xaefY3iN\xf6\xd2S\xfd} \x14\xf4\xe4\xe5I\x02xi\xf8\xf2\xa6!Z\xca\x95\x1bn\xc3\xa6\x0c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

class User(db.Model):
	__tablename__ = 'users'
	username = db.Column(db.String, primary_key=True)
	password = db.Column(db.String)
	authenticated = db.Column(db.Boolean, default=False)
	clearance = db.Column(db.Integer, default=0)
	role = db.Column(db.String, default="user")
	
	def is_active(self):
		return True

	def get_id(self):
		return self.username
		
	def is_authenticated(self):
		return self.authenticated
	
	def is_anonymous(self):
		return False
		
@loginmanager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

@loginmanager.unauthorized_handler
def unauthorized():
	return render_template("unauthorized.html"), 401

def roleunauthorized():
	return render_template("userunauthorized.html"), 401

@app.route('/index')
@app.route('/')
def index():
	if(current_user == None or current_user.is_anonymous == True):
		return("IN DEVELOPMENT",200)
	else:
		return("Welcome " + current_user.username, 200)
@app.route('/files/<fileR>')
@login_required
def Wfile(fileR):
	try:
		xmfile = ET.parse(fileR+".xml")
	except:
		return("File not found", 404)
	
	root = xmfile.getroot()

	doclvl = root.attrib["level"]
	if int(current_user.clearance) < int(doclvl) and doclvl != 0:
		return roleunauthorized()
	txtdata = root[0]
	data = ""
	for child in txtdata.iter():
		if(child.tag == "text"):
			continue
		if(child.tag == "redact"):
			if(int(child.attrib["level"]) <= int(current_user.clearance)):
				data = data + child.text + " "
			else:
				data = data + "REDACTED "
		else:
			data = data + child.text + " "
	return render_template("fileR.html",title=fileR,text=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
# Here we use a class of some kind to represent and validate our
# client-side form data. For example, WTForms is a library that will
# handle this for us, and we use a custom LoginForm to validate.
	form = LoginForm()
	if request.method == "POST":
		user = User.query.get(form.username.data)
		if user == None:
			return render_template("login.html", form=form)
		if bcrypt.check_password_hash(user.password, form.password.data): 
			user.authenticated = True 
			db.session.add(user)
			db.session.commit()
			login_user(user, remember=True)
			flash('Logged in successfully.')

		next = request.args.get('next')
# See http://flask.pocoo.org/snippets/62/ for an example. FIGURE OUT HOW TO DO is_safe_url

		return redirect(next or url_for('index'))
	return render_template('login.html', form=form)

@app.route('/logout',methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect("index")

if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0',debug=True,port=8000)
	except(KeyboardInterrupt):
		exit()