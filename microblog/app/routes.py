from app import app, db
from flask import render_template
from app.forms import LoginForm
from flask import flash, redirect
from flask import url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User

@app.route('/')
def home():
    return "Hellow this is the home page"

@app.route('/index')
@login_required
def index():
#so instead of writing the html code like this without any autofill options we can use templates to seperate these files and import them later.
    user = {'username': 'Isildur'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Hardest choices require the strongest wills!'
        },
        {
            'author': {'username': 'Erika'},
            'body': 'From a place that u wont see, comes a sound that u wont hear, just a flash of light!'
        },
        {
            'author': {'username': 'Thanos'},
            'body': 'You could not live with your own faliure, and where did that bring you? back to me.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

    

@app.route('/login', methods=['GET', 'POST']) #view function accepts GET and POST requests 
def login():
    if current_user.is_authenticated: #if the user is already logged in then user shouldn't navigate to login url of the application 
        #current_user variable comes from Flask-login, and is_authenticated is one of four propreties that we checked with class Mixin
        return redirect(url_for('index'))
    form = LoginForm() #created instance of the form needed for login.html
    if form.validate_on_submit(): #does all the form processing work
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid User name or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #login_user is also a flask-login inbuilt function
        # this line is now replaced with real login connected to database --> flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}') 
        # flash stores the measage in the session and it was displayed using HTML in login.html 
        #flashed messages appear only once after the flash() function is called and the are removed after the get_flashed_messages function
        return redirect(url_for('index')) #if block is executed only when
                                        #>> the form was submitted (method == post) and all fields pass validation
    return render_template('login.html', title='Sign In', form=form)
# if the form had erros or hasn't submitted or hasn't validated properly then the return render_template will just show the loging page again
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
