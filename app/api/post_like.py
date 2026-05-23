from app.database.models import PostLike, UserProfile, Post
from app.database.schema import PostLikeOutSchema, PostLikeInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter, status

post_like_router = APIRouter(prefix='/post_like')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_like_router.post('/', response_model=PostLikeOutSchema, summary='Like the post', tags=['PostLike'])
async def like_post(post_like: PostLikeInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==post_like.user_id).first()
    if not user_db:
        raise HTTPException(detail=f'No user with id {post_like.user_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    post_db = db.query(Post).filter(Post.id==post_like.post_id).first()
    if not post_db:
        raise HTTPException(detail=f'No post with id {post_like.post_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    like_exists = db.query(PostLike).filter(
        PostLike.user_id==post_like.user_id,
        PostLike.post_id==post_like.post_id
    ).first()
    if like_exists:
        raise HTTPException(detail='U are already liked this post',
                            status_code=status.HTTP_409_CONFLICT)

    post_like_db = PostLike(**post_like.model_dump())
    db.add(post_like_db)
    db.commit()
    db.refresh(post_like_db)
    return post_like_db

@post_like_router.get('/{post_id}/get', response_model=List[PostLikeOutSchema], summary='Get all post likes', tags=['PostLike'])
async def posts_likes(post_id: int, db: Session = Depends(get_db)):
    return db.query(PostLike).filter(PostLike.post_id==post_id).limit(100).offset(0).all()

@post_like_router.delete('/{post_id}/delete', response_model=dict, summary='Delete posts like', tags=['PostLike'])
async def posts_like_delete(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post_like_db = db.query(PostLike).filter(
        PostLike.post_id==post_id,
        PostLike.user_id==user_id
    ).first()
    if not post_like_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No likes on this post by this user')

    db.delete(post_like_db)
    db.commit()
    return {'detail': 'Posts like has been deleted'}