from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField


class TopCities(FlaskForm):
    city_name = StringField('city_name')
    city_rank = PasswordField('city_rank')
    is_visited = BooleanField('is_visited')
    comments = StringField('comments')
    submit = SubmitField('Submit')
