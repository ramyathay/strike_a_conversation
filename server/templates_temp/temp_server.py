from flask import Flask, render_template, request, redirect,flash,session,Response,make_response,jsonify
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import Model
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask.ext.cors import CORS,cross_origin
from sqlalchemy.orm import sessionmaker,joinedload,contains_eager
#from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.sql import func
import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_For_Wallapp'
app.config['CORS_HEADERS'] = 'Content-Type'
bcrypt = Bcrypt(app)
cors = CORS(app,resources = r'*')

#SqlAlchemy configurations for mysql db 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/wall_db'
db = SQLAlchemy(app)

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine('mysql+pymysql://root:root@localhost:3306/wall_db')
Session = sessionmaker(bind=engine)


# reflect the tables
Base.prepare(engine, reflect=True)
# mapped classes are now created with names by default matching that of the table name.
Users = Base.classes.users
Posts = Base.classes.posts
Comments = Base.classes.comments
	
sql_alchemy_session = Session()

@app.route('/')
def index():
	#db.create_all()
	return "ramyatha"

@app.route('/registerUser',methods = ['POST'])
def register():
	user_info = {
	'first_name': request.form.get('first_name'),
	'last_name': request.form.get('last_name'),
	'email': request.form.get['email'],
	'password': request.form.get['password'],
	'password_cnf': request.form.get['confirm_password']
	}
	print("Username is ",request.form.get('first_name'))
	user_status = validate_user(user_info)
	if user_status['flag'] == True :
			# for message in user_status['errors']:
			# 	flash(message,'registration_errors')
		return redirect('/')
	else :
		current_time = func.now()
		pw_hash=bcrypt.generate_password_hash(request.form['password'])
		user = Users(first_name = request.form['first_name'],last_name = request.form['last_name'],email = request.form['email'],password = pw_hash,created_at = current_time,updated_at = current_time)
		session['current_user'] = request.form['first_name']
		db.session.add(user)
		db.session.commit()
		return redirect('/success')

@app.route('/loginUser',methods = ["POST"])
def login():
	login_info = {
	'email': request.form['email'],
	'password': request.form['password']
	}
	login_status = login_user(login_info)
	if login_status['loginflag'] == False:
		session['current_user'] = login_status['user_name']
		return redirect('/success')
	else:
		for message in login_status['errors']:
			flash(message,'login_errors')
		return redirect('/')

@app.route('/success')
def success_page():
	return render_template("wall_page.html")  

@app.route('/logoff')
def homepage():
	return redirect('/')	


def validate_user(user_info):
	EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
	flag = False
	errors=[]

	if len(user_info['first_name']) == 0 :
	    errors.append("First Name cannot be empty") 
	    flag=True
	elif len(user_info['first_name']) < 2:
	    errors.append('First Name must be atleast 2 characters')
	    flag=True
	elif (user_info['first_name']).isdigit() :
	    errors.append("First name should contain only alphabets")
	    flag=True

	if len(user_info['last_name']) == 0 :
	    errors.append("Last Name cannot be empty")
	    flag=True 
	elif len(user_info['last_name']) < 2:
	    errors.append('Last Name must be atleast 2 characters')
	    flag=True
	elif (user_info['last_name']).isdigit() :
	    errors.append("Last name should contain only alphabets")
	    flag=True

	if len(user_info['email']) == 0:
	    errors.append('Email field cannot be empty')
	    flag=True
	elif not EMAIL_REGEX.match(user_info['email']):
	    errors.append('Invalid Email!')
	    flag=True

	if len(user_info['password']) ==0 :
	    errors.append("Password field cannot be empty")
	    flag=True
	elif len(user_info['password']) < 8 :
	    errors.append("Password should be 8 characters long")
	    flag=True

	if user_info['password'] != user_info['password_cnf']:
	    errors.append('Password and Confirm passwords should be the same')
	    flag=True

	if errors:
	    return {"flag":True,"errors":errors}
	else:
	    return {"flag":False}

def login_user(login_info):
	errors=[]
	loginflag=False
	result = sql_alchemy_session.query(Users).filter(Users.email == login_info['email']).first()
	#result = sql_alchemy_session.query(Users).get(13)
	#convert the result returned by query operation which is an object to a dictonary
	user_details = result.__dict__
	print("result is",user_details)
	if result == None :
	    loginflag=True
	    errors.append("User does not exist for the given details")
	elif not bcrypt.check_password_hash(user_details['password'],login_info['password']):
	    loginflag=True
	    errors.append("Email and Password do not match")

	if not loginflag:
	    return {"loginflag":False,"user_name":user_details['first_name']} 
	else:
	    return {"loginflag":True,"errors":errors}

@app.route('/currentUser')
def get_currentUser():
	#Query on the columns rather than the entire table to get all columns from both the tables
	result = sql_alchemy_session.query(Posts.post_id,Posts.post_text,Users.first_name).join(Users).all()
	print("TYpe of result is",type(result))
	for user_post in result:
		print("Result of join is",user_post.post_text,user_post.first_name)
		# for post_comment in user_post.post:
		# 	print("Post_comment is",post_comment.post_text)
	return "ramyatha"

@app.route('/userPost',methods = ['POST'])
def userPost():
	print("Entered function")
	print request.json
	# print("text is",request.args['post_message'])
	# userPost_Info = {
	# 'user_id': 14,
	# 'post_text': request.args['post_message']
	# }

	#result = sql_alchemy_session.query(Users).get(14)
	current_time = func.now()
	post = Posts(post_text = request.json['post_message'],created_at = current_time, updated_at = current_time,user_id = 14)
	db.session.add(post)
	db.session.commit()
	# resp = make_response()
	# resp.headers['Access-Control-Allow-Origin'] = '*'
	# return resp
	return jsonify({'success': True})

#store the user_id and first name of the logged in user
app.run(debug = True)











