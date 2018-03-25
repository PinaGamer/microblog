from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5
import random

#Auxiliar tables
followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)	
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	age = db.Column(db.SmallInteger())
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	followed = db.relationship(
		argument='User',									#The right side of the relationship
		secondary=followers,								#Which table holds this relationship
		primaryjoin=(followers.c.follower_id == id),		#The join condition for the left side
		secondaryjoin=(followers.c.followed_id == id),		#The join condition for the right side
		backref=db.backref('followers', lazy='dynamic'), 	#How the relationship will be accesed from the right side
		lazy='dynamic'										#
		)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def forgot_password_generate(self, length=None):
		new_password = ""
		possibleValues = "abcdefghijklmnopqrstuvwxyz"
		if length is None:
			length = 4
		for i in range(length):
			new_password = new_password + possibleValues[random.randint(0, len(possibleValues))]
		return new_password

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(
				followers.c.followed_id == user.id).count() > 0

	def get_followed(self):
		return self.followed

	def get_followers(self):
		return self.followers

	def followed_posts(self):
		followed = Post.query.join(
				followers,(followers.c.followed_id == Post.user_id)).filter(
					followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))