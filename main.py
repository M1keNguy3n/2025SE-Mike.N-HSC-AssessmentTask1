from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import os
from flask_wtf import CSRFProtect
import logging
import userManagement as dbHandler
from userManagement import User
from flask_cors import CORS
import qrcode
import pyotp
from forms import LoginForm, RegistrationForm, TwoFactorForm, Setup2FAForm, DiaryEntryForm
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


@login_manager.user_loader
def load_user(user_id):
    user = dbHandler.get_user_by_id(user_id)
    if user:
        return User(user.id, user.email, user.password, user.otp_secret)
    return None


#register implementation
#Create a registration form using Flask-WTF

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
            session['pre_2fa_user_id'] = user.id
            return redirect(url_for('two_factor'))
        else:
        # Flash message if login fails
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/two_factor', methods=['GET', 'POST'])
def two_factor():
    form = TwoFactorForm()
    if 'pre_2fa_user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['pre_2fa_user_id']
    user = dbHandler.get_user_by_id(user_id)
    
    if form.validate_on_submit():
        token = form.token.data
        if user.verify_totp(token):
            login_user(user)
            session.pop('pre_2fa_user_id', None)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA token. Please try again.', 'danger')
    return render_template('two_factor.html', form=form)

    
@app.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    if 'pre_2fa_user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['pre_2fa_user_id']
    user = dbHandler.get_user_by_id(user_id)
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        dbHandler.update_user_otp_secret(user_id, user.otp_secret)
    uri = user.get_totp_uri()
    img = qrcode.make(uri)
    
    # Ensure the static/qrcodes directory exists
    qr_code_dir = os.path.join(app.static_folder, 'qrcodes')
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)
    
    # Save the QR code image
    img_path = os.path.join(qr_code_dir, f'{user_id}.png')
    img.save(img_path)
    
    form = Setup2FAForm()
    if form.validate_on_submit():
        flash('2FA setup complete. You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('setup_2fa.html', user_id=user_id, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        otp_secret = pyotp.random_base32()

        # Check if the user already exists
        existing_user = dbHandler.get_users(email)
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))
            
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        # Insert the user into the database
        dbHandler.insert_users(email, hashed_password, otp_secret)
        flash('Registration successful! Please setup 2FA.', 'success')
        session['pre_2fa_user_id'] = dbHandler.get_users(email).id
        
        # Redirect to 2FA setup
        return redirect(url_for('setup_2fa'))
    
    return render_template('register.html', form=form)


#diary entry implementation

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
