#!/bin/sh
if [ $0 == $BASH_SOURCE ]; then
	echo "Execute with the 'source' command instead 'bash'"
else
	echo "Ejecucion de tareas previas a la inicializacion del proyecto"
	echo 	"Activando el entorno virtual...
		source venv/bin/activate"
	source venv/bin/activate
	echo 	"Exportando la variable FLASK_APP...
		export FLASK_APP=microblog.py"
	export FLASK_APP=microblog.py
	echo 	"Exportando la variable FLASK_DEBUG...
		export FLASK_DEBUG=1"
	export FLASK_DEBUG=1
	echo "Finalizado :)"
fi
