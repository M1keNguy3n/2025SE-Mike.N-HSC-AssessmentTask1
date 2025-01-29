from flask import Flask, redirect, render_template, request, jsonify, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, URLField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL
import os
from flask_wtf import CSRFProtect
import logging
import userManagement as dbHandler
from userManagement import User
from flask_cors import CORS

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a 24 byte secret key
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)
CORS(app, origins=[r'.*\.github\.dev'])

@app.route('/static/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

#apply_csp after every request
@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = (
        "base-uri 'self' https://github.dev; "
        "default-src 'self' https://github.dev;"
        "style-src 'self' https://github.dev; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "media-src 'self'; "
        "font-src 'self'; "
        "object-src 'self'; "
        "child-src 'self'; "
        "connect-src 'self'; "
        "worker-src 'self'; "
        "report-uri /csp_report; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "frame-src 'none';"
        )
    return response

# login implementation
users = {}
login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message='Password must be between 8 and 20 characters')])
    submit = SubmitField('Sign In')


@login_manager.user_loader
def load_user(user_id):
    return dbHandler.get_user_by_id(user_id)


#register implementation
#Create a registration form using Flask-WTF
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 20, message='Password must be between 8 and 20 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min = 8, max = 20, message='Password must be between 8 and 20 characters')])
    submit = SubmitField('Register')

@app.route("/", methods=["GET"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Check if user exists and password is correct
        user = dbHandler.get_users(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
        # Flash message if login fails
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if the user already exists
        if email in users:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))
            
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Create a new user and store it in memory (for demonstration)
        user = User(email, generate_password_hash(password))
        dbHandler.insert_users(user.id, user.password)
        flash('Registration successful! You can now log in.', 'success')
        
        # Redirect to the login page after successful registration
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


#diary entry implementation
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

@app.route('/new_entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = DiaryEntryForm()
    if request.method == "POST" and form.validate_on_submit():
        developer = form.developer.data
        project = form.project.data
        start_time = form.start_time.data.strftime('%Y-%m-%d %H:%M:%S')
        end_time = form.end_time.data.strftime('%Y-%m-%d %H:%M:%S')
        repo_url = form.repo_url.data
        dev_note = form.dev_note.data
        code_snippet = form.code_snippet.data
        language = form.language.data
        dbHandler.insert_diaries(developer, project, start_time, end_time, repo_url, dev_note, code_snippet, language)
        
        flash('Diary entry submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html', form=form)

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/index", methods=['GET'])

def index():
    return render_template("/index.html", content= dbHandler.list_diaries())

@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template("/dashboard.html", content= dbHandler.list_diaries())

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['FLASK_DEBUG'] = 1
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=5000)
