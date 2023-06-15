setup: requirements.txt
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	pip install -r requirements.txt

setup-lin: requirements.txt
	python -m venv env
	source ./env/Scripts/activate
	pip install -r requirements.txt

run-cli:
	python ap_proc.py test

run-server:
	flask --debug run --host=0.0.0.0
