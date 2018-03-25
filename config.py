import os

class Config(object):
	#SECRET_KEY es una variable de entorno
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'