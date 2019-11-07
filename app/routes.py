from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User, Project, Todo
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

#home page. Shows all existing projects in the database
@app.route('/')
@app.route('/index')
@login_required 
def index():
    user = User.query.filter_by(username=current_user.username).first()
    projects = user.projects.all()
    #todo = user.todo.all()
    return render_template('index.html', title='Home', projects=projects)

#login page.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # look at first result first()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return to page before user got asked to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/project/<id>')
def project(id):
    current_project = current_user.projects.filter_by(id=int(id)).first()
    todo = current_project.todos.all()
    return render_template('project.html', project=current_project, tasks=todo)
    #return '<h1>{}</h1>'.format(current_project.name)

#routes to a new page that grabs input from the user
@app.route('/create') #create tasks
def create():
    return render_template('create.html')

#/create redirects user to this url. A new project is created and added to the database in this url    
@app.route('/addProject', methods=['POST']) #create tasks
def addProject():
    project = Project(name=request.form['Project name'])
    db.session.add(project)
    project.contributors.append(current_user)
    db.session.commit()
    return redirect(url_for('index'))

#clicking the add task button will route you here. A task is created and added to the database here.
@app.route('/addTask/<id>', methods=['POST']) #create tasks
def addTask(id):
    current_project = current_user.projects.filter_by(id=int(id)).first()
    todo = Todo(task=request.form['task'], project=current_project)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('project', id=id))


