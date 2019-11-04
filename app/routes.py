from flask import render_template
from app import myApp

@myApp.route('/')
def front():
	return render_template('index.html')
		