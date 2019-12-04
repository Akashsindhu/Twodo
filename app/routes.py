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

# home page. Shows all existing projects in the database
@app.route('/')
@app.route('/index')
@login_required

def index():
    # grab the current user by filtering through all the users
    user = User.query.filter_by(username=current_user.username).first()
    # grab the list of projects that the current user has
    projects = user.projects.all()
    return render_template('index.html', title='Home', projects=projects)


# login page.
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


# prints the list of tasks within a project
@app.route('/project/int:<id>')
def project(id):
    # grab current project. Filters the list using the unique id belonging to the project.
    # refer to models.py to see all the attributes of each database
    current_project = current_user.projects.filter_by(id=id).first()
    # separate incomplete and complete projects using the 'complete' attribute that is unique to each todo item
    incomplete = current_project.todos.filter_by(complete=False).all()
    complete = current_project.todos.filter_by(complete=True).all()
    contributors = current_project.contributors.all()
    # pass in the incomplete and complete items into the render function
    return render_template('project.html', project=current_project, complete=complete, incomplete=incomplete, contributors=contributors)
    # return '<h1>{}</h1>'.format(current_project.name)


# routes to a new page that grabs input from the user
@app.route('/create')  # create tasks
def create():
    # create.html is the page that takes in the project name and routes to /addProject
    return render_template('create.html')


# /create redirects user to this url. A new project is created and added to the database in this url
@app.route('/addProject', methods=['POST'])  # create tasks
def addProject():
    # create a new Project using the name inputted in create.html
    project = Project(name=request.form['Project name'])
    # add to database
    db.session.add(project)
    # update list of contributors for the Project
    project.contributors.append(current_user)
    db.session.commit()
    return redirect(url_for('index'))


# clicking the add task button will route you here. A task is created and added to the database here
@app.route('/addTask/int:<id>', methods=['POST'])  # create tasks
def addTask(id):
    # grab current project by filter by id
    current_project = current_user.projects.filter_by(id=id).first()
    # create a new Todo. This Todo will be added to the database. The text is grabbed from project.html
    todo = Todo(task=request.form['task'], project=current_project)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('project', id=id))


# deletes a task from the database. project_id and task id must be passed into this function
@app.route('/deleteTask/int:<project_id>/int:<task_id>', methods=['POST'])  # delete tasks
def deleteTask(project_id, task_id):
    current_project = current_user.projects.filter_by(id=project_id).first()
    task = current_project.todos.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('project', id=current_project.id))


# marks a task as complete by changing the 'complete' attribute to True
@app.route('/complete/int:<project_id>/int:<task_id>', methods=['POST'])
def complete(project_id, task_id):
    current_project = current_user.projects.filter_by(id=project_id).first()
    task = current_project.todos.filter_by(id=task_id).first()
    task.complete = True
    db.session.commit()

    return redirect(url_for('project', id=current_project.id))


@app.route('/deleteProject/int:<project_id>', methods=['POST'])  # delete project
def deleteProject(project_id):
    current_project = current_user.projects.filter_by(id=project_id).first()
    db.session.delete(current_project)
    db.session.commit()

    return redirect(url_for('index', id=current_project.id))

@app.route('/addContributor/int:<project_id>', methods=['POST'])  # create tasks
def addContributor(project_id):
    # create a new Project using the name inputted in create.html
    user = User.query.filter_by(username=request.form['contributor']).first()
    current_project = current_user.projects.filter_by(id=project_id).first()
    # add to database
    current_project.contributors.append(user)
    # update list of contributors for the Project
    db.session.commit()
    return redirect(url_for('project', id=current_project.id))
