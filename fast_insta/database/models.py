from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Date, Text, Enum, Boolean
from typing import List
from enum import Enum as PyEnum
from datetime import date

class StatusChoices(str, PyEnum):
    PRO = 'Pro'
    SIMPLE = 'Simple'

class UserProfile(Base):
    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.SIMPLE)
    data_registered: Mapped[date] = mapped_column(Date, default=date.today)

    follower_user: Mapped[List['Follow']] = relationship(back_populates='follower',
                                                   cascade='all, delete-orphan', foreign_keys='Follow.follower_id')
    following_user: Mapped[List['Follow']] = relationship(back_populates='following',
                                                    cascade='all, delete-orphan', foreign_keys='Follow.following_id')
    post_user: Mapped[List['Post']] = relationship(back_populates='user',
                                             cascade='all, delete-orphan')
    post_like_user: Mapped[List['PostLike']] = relationship(back_populates='user',
                                                       cascade='all, delete-orphan')
    comment_user: Mapped[List['Comment']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')
    comment_like_user: Mapped[List['CommentLike']] = relationship(back_populates='user',
                                                                  cascade='all, delete-orphan')
    users_token: Mapped[List['UserProfileRefreshToken']] = relationship(
        back_populates='token_user',
        cascade='all, delete-orphan'
    )

class UserProfileRefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    token_user: Mapped[UserProfile] = relationship(back_populates='users_token')

class Follow(Base):
    __tablename__ = 'follow'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    following_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    followed_date: Mapped[date] = mapped_column(Date, default=date.today)

    follower: Mapped[UserProfile] = relationship(back_populates='follower_user', foreign_keys=[follower_id])
    following: Mapped[UserProfile] = relationship(back_populates='following_user', foreign_keys=[following_id])

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    hashtag: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped[UserProfile] = relationship(back_populates='post_user')
    post_like: Mapped['PostLike'] = relationship(back_populates='post')
    comment_post: Mapped['Comment'] = relationship(back_populates='post')

class PostLike(Base):
    __tablename__ = 'post_like'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[UserProfile] = relationship(back_populates='post_like_user')
    post: Mapped[Post] = relationship(back_populates='post_like')

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped[UserProfile] = relationship(back_populates='comment_user')
    post: Mapped[Post] = relationship(back_populates='comment_post')
    comment_like: Mapped['CommentLike'] = relationship(back_populates='comment')

class CommentLike(Base):
    __tablename__ = 'comment_like'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'))
    like: Mapped[bool] = mapped_column(Boolean)

    user: Mapped[UserProfile] = relationship(back_populates='comment_like_user')
    comment: Mapped[Comment] = relationship(back_populates='comment_like')