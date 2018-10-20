clean: 
	@find . -name "*.pyc" -delete

runserver:
	@python server.py

sendfile: 
	@python client.py $(file) 
