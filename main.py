from flask import Flask, redirect, render_template, request, jsonify, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os
from flask_wtf import CSRFProtect
import logging
import userManagement as dbHandler
from userManagement import User

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

#apply_csp after every request
@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = (
        "base-uri 'self'; "
        "default-src 'self'; "
        "style-src 'self'; "
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


@login_manager.user_loader
def load_user(user_id):
    return dbHandler.get_user_by_id(user_id)


#register implementation
#Create a registration form using Flask-WTF
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.errors)
        email = form.email.data.strip()
        password = form.password.data.strip()
        print('email and password received')
        # Check if user exists and password is correct
        user = dbHandler.get_users(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        
        # Flash message if login fails
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()
        confirm_password = form.confirm_password.data.strip()

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
        return redirect(url_for('login.html'))
    
    return render_template('register.html', form=form)



# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/index", methods=['GET'])
@app.route("/", methods=["GET"])
def index():
    print("i was here")
    return render_template("/index.html", content= dbHandler.list_diaries_collapsed())


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


# example CSRF protected form
@app.route("/form.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        email = request.form["email"]
        text = request.form["text"]
        return render_template("/form.html")
    else:
        return render_template("/form.html")


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
