from flask import Flask, redirect
from flask import render_template

# uncomment line below once you have created the
# TopCities class inside the form.py file
from form import TopCities

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-key'

@app.route('/body1', methods=['GET', 'POST'])
def home1():
    title = 'Home'
    top_cities = ['Paris', 'London', 'Rome', 'Tahiti']
    form = TopCities()
    return render_template('home.html', title = title, name='Home', topcty=top_cities, form=form)


@app.route('/body2/<name>', methods=['GET', 'POST'])
def home(name):

    top_cities = ['Paris', 'London', 'Rome', 'Tahiti']
    title='top cities'
    form = TopCities()

    return render_template('home.html', title=title, name=name, topcty=top_cities, form=form)


if __name__ == '__main__':
    app.run(debug=True)