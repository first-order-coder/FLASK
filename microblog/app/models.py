from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model): #if db.Model isn't used then all the mappings have to be done manually
    __tablename__ = 'db_User'
    id: so.Mapped[int] = so.mapped_column(primary_key=True) #these are python type hints
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True) #stores string upto 64 characters and indexed for fast lookup and is unique no duplicate usernames

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)


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