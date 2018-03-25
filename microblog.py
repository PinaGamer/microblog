from app import app,db		#Importa del paquete app la variable app que representa la instancia de Flask
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post' : Post}

