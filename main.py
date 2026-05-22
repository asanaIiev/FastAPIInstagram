from fastapi import FastAPI
from fast_insta.admin.setup import admin_setup
from fast_insta.api import auth, user_profile, follow, post, post_like, comment_like, comment
import uvicorn
app = FastAPI()
app.include_router(auth.auth_router)
app.include_router(user_profile.users_router)
app.include_router(follow.follow_router)
app.include_router(post.post_router)
app.include_router(post_like.post_like_router)
app.include_router(comment.comment_router)
app.include_router(comment_like.comment_like_router)

admin_setup(app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)