from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message='Password must be between 8 and 20 characters')])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 20, message='Password must be between 8 and 20 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min = 8, max = 20, message='Password must be between 8 and 20 characters')])
    submit = SubmitField('Register')

class TwoFactorForm(FlaskForm):
    token = StringField('Enter 2FA Token', validators=[DataRequired()])
    submit = SubmitField('Verify')

class TwoFactorForm(FlaskForm):
    token = StringField('Enter 2FA Token', validators=[DataRequired()])
    submit = SubmitField('Verify')

class Setup2FAForm(FlaskForm):
    submit = SubmitField('Complete Setup')

class DiaryEntryForm(FlaskForm):
    developer = StringField('Developer', validators=[DataRequired(), Length(min=2, max=50, message='Developer name must be between 2 and 50 characters')])
    project = StringField('Project', validators=[DataRequired(), Length(min=2, max=100, message='Project name must be between 2 and 100 characters')])
    start_time = DateTimeField(
        'Start Time', 
        validators=[DataRequired(message='Please enter a valid date and time.')],
        format='%Y-%m-%d %H:%M:%S',
        render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"},
    )
    end_time = DateTimeField(
        'End Time', 
        validators=[DataRequired(message='Please enter a valid date and time.')],
        format='%Y-%m-%d %H:%M:%S',
        render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"},
    )
    repo_url = URLField(
        'Repository URL',
        validators=[DataRequired(), URL(message='Please enter a valid URL')])
    dev_note = TextAreaField(
        'Developer Note',
        validators=[DataRequired(), Length(max=2000, message='Developer note must be less than 2000 characters')]
    )
    code_snippet = TextAreaField(
        'Code Snippet',
        validators=[DataRequired(), Length(max=2000, message='Code snippet must be less than 2000 characters')]
    )
    language = SelectField(
        'Language',
        choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('html', 'HTML')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')