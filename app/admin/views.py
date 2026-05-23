from app.database.models import *
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = []
    for i in UserProfile.__mapper__.columns: column_list.append(i.key)

class UserProfileRefreshAdmin(ModelView, model=UserProfileRefresh):
    column_list = [i.key for i in UserProfileRefresh.__mapper__.columns]

class FollowAdmin(ModelView, model=Follow):
    column_list = [i.key for i in Follow.__mapper__.columns]

class PostAdmin(ModelView, model=Post):
    column_list = [i.key for i in Post.__mapper__.columns]

class PostLikeAdmin(ModelView, model=PostLike):
    column_list = [i.key for i in PostLike.__mapper__.columns]

class CommentAdmin(ModelView, model=Comment):
    column_list = [i.key for i in Comment.__mapper__.columns]

class CommentLikeAdmin(ModelView, model=CommentLike):
    column_list = [i.key for i in CommentLike.__mapper__.columns]