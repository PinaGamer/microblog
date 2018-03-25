from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from wtforms.widgets import *
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email(message="Use a valid email")])	#El segundo validator Email() asegura que el usuario introduce un string con el formato de una direccion de correo
	age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, message="You must be over 18")])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address')

class EditProfileForm(FlaskForm):
	username = StringField('Username')
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	email = StringField('Email', validators=[Email(message="Use a valid email"), DataRequired()])
	age = IntegerField('Age', validators=[NumberRange(min=18, message="You must be over 18")])
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username')

