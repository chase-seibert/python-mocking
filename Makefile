test:
	@. venv/bin/activate; nosetests
venv:
	@test -d venv || virtualenv venv
	@. venv/bin/activate; pip install -r requirements.txt
	@touch venv/bin/activate
