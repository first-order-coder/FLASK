from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! its the first deployment"