from sqladmin import Admin
from app.database.db import engine
from .views import *
from fastapi import FastAPI

def admin_setup(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(UserProfileRefreshAdmin)
    admin.add_view(FollowAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(PostLikeAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(CommentLikeAdmin)