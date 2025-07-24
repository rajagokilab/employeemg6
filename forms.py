from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import InputRequired

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    position = StringField('Position', validators=[InputRequired()])
    department = StringField('Department', validators=[InputRequired()])
    salary = FloatField('Salary', validators=[InputRequired()])
    submit = SubmitField('Submit')
