from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ColumnSearchForm(FlaskForm):
    search_term = StringField(label="Search Term", validators=[DataRequired()])
    where_term = StringField(label="Where Term")

    submit = SubmitField(label='Search')
