from flask import Flask, render_template, request, redirect,flash,session,Response,make_response,jsonify
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import Model
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask.ext.cors import CORS,cross_origin
from sqlalchemy.orm import sessionmaker,joinedload,contains_eager
#from sqlalchemy.orm import Session
from sqlalchemy import create_engine,desc
from sqlalchemy import *
from sqlalchemy.sql import func
import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_For_Wallapp'
bcrypt = Bcrypt(app)
CORS(app)

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
	return "Hello Ramyatha!"

@app.route('/users',methods = ["POST"])
def create_user():
	current_time = func.now()
	user = Users(first_name = request.json['first_name'],last_name = request.json['last_name'],email = request.json['email'],password = request.json['password'],created_at = current_time,updated_at = current_time)
	db.session.add(user)
	db.session.commit()
	session['user_id'] = user.user_id
	print("Success User created")
	return jsonify(user_id = user.user_id)

@app.route('/users/<id>')
def get_user_by_id(id):
	user_info = sql_alchemy_session.query(Users).get(id)
	print("get_user" , user_info)
	user = "Requested user is" + user_info.first_name + user_info.last_name
	return user

#@app.route('/users/<id>/posts',methods = ["POST"])
@app.route('/users/posts',methods = ["POST"])
def create_post():
	#id = session['user_id']
	id = 23
	current_time = func.now()
	post = Posts(post_text = request.json['user_post'],created_at = current_time, updated_at = current_time,user_id = id)
	sql_alchemy_session.add(post)
	sql_alchemy_session.commit()
	print("Successfully posted the message")
	return jsonify(post_id = post.post_id )

@app.route('/users/posts/comments')
def get_all_users_posts():
	all_user_posts = []
	all_comments = []
	posts_and_users = sql_alchemy_session.query(Posts.post_id,Posts.post_text,Posts.created_at,Users.first_name,Users.last_name,Users.user_id).join(Users).order_by(Posts.created_at.desc()).all()
	posts_and_comments = sql_alchemy_session.query(Posts.post_id,Posts.post_text,Comments.comment_id,Comments.comment_text,Comments.created_at).join(Comments).all()
	comments_and_users = sql_alchemy_session.query(Comments.comment_id,Users.first_name,Users.last_name,Users.user_id).join(Users).all()
	for post_data in posts_and_users:
		for comment_data in posts_and_comments:
			if post_data.post_id == comment_data.post_id :
				for user_data in comments_and_users:   #Is there a need for third loop to get comment user info?
					if user_data.comment_id == comment_data.comment_id:	
						all_comments.append({'comment_text': comment_data.comment_text,'comment_created_at': comment_data.created_at,'commented_by': user_data.first_name + " " + user_data.last_name,'user_id': user_data.user_id})
		all_posts = {
			'first_name': post_data.first_name,
			'last_name': post_data.last_name,
			'user_id': post_data.user_id,
			'post_text': post_data.post_text,
			'post_created_at': post_data.created_at,
			'posted_by': post_data.first_name + " "+ post_data.last_name,
			'post_id': post_data.post_id,
			'comments': all_comments
		}
		all_comments = []  #Is it the right way to remove data from an array and reassign it?
		all_user_posts.append(all_posts)

	print("All posts are" ,all_user_posts)
	return jsonify(result = all_user_posts)

#@app.route('/users/<user_id>/posts/<post_id>/comments',methods = ["POST"])
@app.route('/users/posts/<id>/comments',methods = ["POST"])
def create_comments(id):
	current_time = func.now()
	user_id = 14
	comment = Comments(comment_text = request.json['user_comment'],created_at = current_time, updated_at = current_time,user_id = 14,post_id = id)
	sql_alchemy_session.add(comment)
	sql_alchemy_session.commit()
	return jsonify(comment_id = comment.comment_id)

@app.route('/users/posts/<id>',methods = ["DELETE"])
def delete_post(id):
	post_by_id = sql_alchemy_session.query(Posts).get(id)
	sql_alchemy_session.delete(post_by_id)
	sql_alchemy_session.commit()
	return jsonify(result = "Post deleted Successfully")

@app.route('/users/posts/<post_id>/comments/<comment_id>',methods = ["DELETE"])
def delete_comment(post_id,comment_id):
	comment_by_id = sql_alchemy_session.query(Comments).get(comment_id)
	sql_alchemy_session.delete(comment_by_id)
	sql_alchemy_session.commit()
	return jsonify(result = "Comment deleted Successfully")

@app.route('/users/posts/<id>',methods = ["PUT"])
def update_post(id):
	sql_alchemy_session.query(Posts).filter(Posts.post_id == id).update({"post_text": (request.json['post_text'])})
	sql_alchemy_session.commit()
	return jsonify(result = "Post Updated Successfully")

@app.route('/users/posts/<post_id>/comments/<comment_id>',methods = ["PUT"])
def update_comment(post_id,comment_id):
	sql_alchemy_session.query(Comments).filter(Comments.comment_id == comment_id).update({"comment_text": (request.json['comment_text'])})
	sql_alchemy_session.commit()
	return jsonify(result = "Comment Updated Successfully")

@app.route('/register',methods = ['POST'])
def register():
	user_info = {
	'first_name': request.json['first_name'],
	'last_name': request.json['last_name'],
	'email': request.json['email'],
	'password': request.json['password'],
	'password_cnf': request.json['confirm_password']
	}
	user_status = validate_user(user_info)
	if user_status['flag'] == True :
		return jsonify(error = True)
	else :
		current_time = func.now()
		pw_hash=bcrypt.generate_password_hash(request.json['password'])
		user = Users(first_name = request.json['first_name'],last_name = request.json['last_name'],email = request.json['email'],password = pw_hash,created_at = current_time,updated_at = current_time)
		print("user is",user.__dict__)
		session['current_user'] = request.json['first_name']
		sql_alchemy_session.add(user)
		#Flush() to add the current transaction to the db and get the auto generated user_idfo rthis transaction
		sql_alchemy_session.flush()
		user_id = user.__dict__.get('user_id')
		#commit() commits any pending changes to the db
		sql_alchemy_session.commit()
		return jsonify(error = False,username = session['current_user'],user_id = user_id)

@app.route('/login',methods = ["POST"])
def login():
	login_info = {
	'email': request.json['email'],
	'password': request.json['password']
	}
	login_status = login_user(login_info)
	if login_status['loginflag'] == False:
		session['current_user'] = login_status['user']['first_name']
		return jsonify(errors = False, username = session['current_user'],user_id = login_status['user']['user_id'])
	else:
		for message in login_status['errors']:
			flash(message,'login_errors')
		return jsonify(errors = True)

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
	    return {"loginflag":False,"user": user_details} 
	else:
	    return {"loginflag":True,"errors":errors}

app.run(debug = True)











