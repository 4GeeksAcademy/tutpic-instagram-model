from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column , relationship
from typing import List

db = SQLAlchemy()

Follower = Table(
    "Follower",
    db.metadata,
    Column("user_from_id",ForeignKey("users.id"), primary_key=True),
    Column("user_to_id",ForeignKey("users.id"), primary_key=True),
)

class User(db.Model):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")

    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    followed: Mapped[List["User"]] = relationship("User", secondary = Follower, back_populates="followers")
    followers: Mapped[List["User"]] = relationship("User", secondary = Follower, back_populates="followed")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username":self.username
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__= "posts"

    id:Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200),nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts") 

    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    media: Mapped["Media"] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "title":self.title
        }
    
class Comment(db.Model):
    __tablename__="comments"

    id:Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200),nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id":self.id,
            "comment_text":self.comment_text,
            "post_id":self.post_id,
            "author_id":self.user_id
        }
    
class Media(db.Model):
    __tablename__="media"

    id:Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(150), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return{
            "id":self.id,
            "url":self.url,
            "post_id":self.post_id
        }
