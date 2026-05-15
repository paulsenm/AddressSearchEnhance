from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

import os
from dotenv import load_dotenv
from pathlib import Path

from handle_address import create_address, get_juris_permit_type_blocks
from soap_requests import get_juris_contact

load_dotenv()
FLASK_LOGIN_KEY = os.getenv("FLASK_LOGIN_KEY")

application = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
application.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'database.db'}"
application.config['SECRET_KEY'] = FLASK_LOGIN_KEY
db = SQLAlchemy(application)

bcrypt = Bcrypt(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable=False)

    def __str__(self):
        return f'username: {self.username}, password: {self.password}'

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_check = User.query.filter_by(username=username.data).first()
        if existing_user_check:
            raise ValidationError('That username already exists')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    submit = SubmitField('login')

@application.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)

        print(f'adding {new_user}')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@application.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@application.route('/address_search', methods=['GET','POST'])
@login_required
def address_search():
    if request.method == 'GET':
        return render_template('address_search.html')
    
    address_string = request.form.get('address-input') or ""
    address_object = create_address(address_string)
    juris_permit_type_blocks = get_juris_permit_type_blocks(address_object)
    contact_blocks = []
    for juris_block in juris_permit_type_blocks:
        contact_block = get_juris_contact(juris_block=juris_block)
        contact_blocks.extend(contact_block)
        print(contact_block)
    
    return render_template('address_search.html', contact_blocks = contact_blocks)

@application.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
    application.run()