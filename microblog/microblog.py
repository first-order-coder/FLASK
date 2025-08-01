from app import app,db
from app.models import User, Post
import sqlalchemy as sa
import sqlalchemy.orm as so

#>>> from app import app, db
#>>> from app.models import User, Post
#>>> import sqlalchemy as sa
#>>> app.app_context().push() instead of repeating the above statement everytime when we used the python hell we can use shell context function like 
# app.shell_context_processor decorator registers the function as a shell context function
#when flask shll command runs, it will invoke this function belowe and register the items returned by it in the shell session.

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}