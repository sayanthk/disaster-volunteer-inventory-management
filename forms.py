from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Volunteer', 'Volunteer'), ('Inventory Manager', 'Inventory Manager'), ('Administrator', 'Administrator')], validators=[DataRequired()])
    skills = TextAreaField('Skills (for Volunteers)', validators=[])
    availability = StringField('Availability (e.g. Weekdays, Weekends)', validators=[])
    location = StringField('Location/City', validators=[])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DisasterForm(FlaskForm):
    name = StringField('Disaster Name', validators=[DataRequired(), Length(max=150)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    severity = SelectField('Severity', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], validators=[DataRequired()])
    required_skills = TextAreaField('Required Skills (comma separated)', validators=[])
    submit = SubmitField('Create Disaster Event')

class ResourceForm(FlaskForm):
    name = StringField('Resource Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Medical', 'Medical'), ('Shelter', 'Shelter'), ('Tools', 'Tools')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Resource')

class AllocationForm(FlaskForm):
    resource_id = SelectField('Resource', coerce=int, validators=[DataRequired()])
    disaster_id = SelectField('Disaster Event', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity to Allocate', validators=[DataRequired()])
    submit = SubmitField('Allocate Resource')

class AssignmentForm(FlaskForm):
    volunteer_id = SelectField('Volunteer', coerce=int, validators=[DataRequired()])
    disaster_id = SelectField('Disaster Event', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Volunteer')

class RatingForm(FlaskForm):
    rating_score = SelectField('Rating Score (1-5)', choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')], coerce=int, validators=[DataRequired()])
    remarks = TextAreaField('Remarks / Feedback', validators=[])
    submit = SubmitField('Submit Rating')

class ResourceRequestForm(FlaskForm):
    disaster_id = SelectField('Disaster Event', coerce=int, validators=[DataRequired()])
    resource_id = SelectField('Resource', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit Request')
