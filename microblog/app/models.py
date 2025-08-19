from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model): #if db.Model isn't used then all the mappings have to be done manually
    id: so.Mapped[int] = so.mapped_column(primary_key=True) #these are python type hints
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True) #stores string upto 64 characters and indexed for fast lookup and is unique no duplicate usernames

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
         self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
         password_hash = str(self.password_hash)
         return check_password_hash(password_hash, password)
    
    def avatar(self, size):
          digest = md5(self.email.lower().encode('utf-8')).hexdigest()
          return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
@login.user_loader #user loader function is a built in function in flask
def load_user(id):
     return db.session.get(User, int(id))

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id) , index=True) #foreign key references the primary key of User table
    author: so.Mapped[User] = so.relationship(back_populates='posts') #author.username will point to the username in User class

    def __repr__(self):
          return '<Post {}>'.format(self.body)  
    
# >> app.app_context().push() this command activates the flask application context manually, so Flask-SQLAlchemy know which app your'e referring to even outside the usual request flow

## get all users in reverse alphabetical order
#>>> query = sa.select(User).order_by(User.username.desc())
#>>> db.session.scalars(query).all()
#[<User susan>, <User john>]

# get all users that have usernames starting with "s"
#>>> query = sa.select(User).where(User.username.like('s%'))
#>>> db.session.scalars(query).all()
#[<User susan>]

