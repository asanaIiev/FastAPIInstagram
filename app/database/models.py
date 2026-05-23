from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum, Date, Text, UniqueConstraint
from app.database.db import Base
from typing import List
from enum import Enum as PyEnum
from datetime import date

class StatusChoices(str, PyEnum):
    SIMPLE = 'Simple'
    PRO = 'Pro'

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.SIMPLE)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)

    user_refresh: Mapped['UserProfileRefresh'] = relationship(back_populates='refresh_user',
                                                              cascade='all, delete-orphan')
    user_follower: Mapped[List['Follow']] = relationship(back_populates='follower_user',
                                                   cascade='all, delete-orphan', foreign_keys='Follow.follower_id')
    user_following: Mapped[List['Follow']] = relationship(back_populates='following_user',
                                                    cascade='all, delete-orphan', foreign_keys='Follow.following_id')
    user_post: Mapped[List['Post']] = relationship(back_populates='post_user',
                                             cascade='all, delete-orphan')
    user_post_like: Mapped[List['PostLike']] = relationship(back_populates='post_like_user',
                                                      cascade='all, delete-orphan')
    user_comment: Mapped[List['Comment']] = relationship(back_populates='comment_user',
                                                         cascade='all, delete-orphan')
    user_comment_like: Mapped[List['CommentLike']] = relationship(back_populates='comment_like_user',
                                                                  cascade='all, delete-orphan')

class UserProfileRefresh(Base):
    __tablename__ = 'refresh'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    refresh: Mapped[str] = mapped_column(String)

    refresh_user: Mapped[UserProfile] = relationship(back_populates='user_refresh')

class Follow(Base):
    __tablename__ = 'follow'

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='_follower_following_uc'),
    )

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    following_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    followed_date: Mapped[date] = mapped_column(Date, default=date.today)

    follower_user: Mapped[UserProfile] = relationship(back_populates='user_follower', foreign_keys=follower_id)
    following_user: Mapped[UserProfile] = relationship(back_populates='user_following', foreign_keys=following_id)

class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    hashtag: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    post_user: Mapped[UserProfile] = relationship(back_populates='user_post')
    post_like: Mapped[List['PostLike']] = relationship(back_populates='like_post',
                                                       cascade='all, delete-orphan')
    post_comment: Mapped[List['Comment']] = relationship(back_populates='comment_post',
                                                         cascade='all, delete-orphan')

class PostLike(Base):
    __tablename__ = 'post_like'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    post_like_user: Mapped[UserProfile] = relationship(back_populates='user_post_like')
    like_post: Mapped[Post] = relationship(back_populates='post_like')

class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    comment: Mapped[str] = mapped_column(Text)
    commented_date: Mapped[date] = mapped_column(Date, default=date.today)

    comment_user: Mapped[UserProfile] = relationship(back_populates='user_comment')
    comment_post: Mapped[Post] = relationship(back_populates='post_comment')
    comment_like: Mapped[List['CommentLike']] = relationship(back_populates='like_comment',
                                                             cascade='all, delete-orphan')

class CommentLike(Base):
    __tablename__ = 'comment_like'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    comment_id: Mapped[int] = mapped_column(ForeignKey('comment.id'))
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    comment_like_user: Mapped[UserProfile] = relationship(back_populates='user_comment_like')
    like_comment: Mapped[Comment] = relationship(back_populates='comment_like')