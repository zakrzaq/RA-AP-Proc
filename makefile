setup: requirements.txt
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	pip install -r requirements.txt

setup-lin:
	python -m venv env
	source ./env/Scripts/activate
	pip install -r requirements.txt

run-test:
	python ap_proc.py test

run-prod:
	python ap_proc.py test

run-server:
	flask --debug run --host=0.0.0.0
