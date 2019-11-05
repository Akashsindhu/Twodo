from flask import render_template
from app import myApp
from app.forms import Login

@myApp.route('/')
def front():
	return render_template('index.html')

@myApp.route('/login')
def login():
	form = Login()
	if form.validate_on_submit():
		pass
	return render_template('login.html', form=form)