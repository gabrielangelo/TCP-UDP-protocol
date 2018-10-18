clean: 
	@find . -name "*.pyc" -delete

runserver:
	@python server.py
