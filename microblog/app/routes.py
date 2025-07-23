from app import app
from flask import render_template

@app.route('/')
def home():
    return "Hellow this is the home page"

@app.route('/index')
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