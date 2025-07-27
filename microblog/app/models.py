from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) #these are python type hints
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True) #stores string upto 64 characters and indexed for fast lookup and is unique no duplicate usernames
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    