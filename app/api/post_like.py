from app.database.models import PostLike
from app.database.schema import PostLikeOutSchema, PostLikeInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

post_like_router = APIRouter(prefix='/post_like')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_like_router.post('/', response_model=PostLikeOutSchema, summary='Like the post.', tags=['PostLike'])
async def like_post(post_like: PostLikeInputSchema, db: Session = Depends(get_db)):
    post_like_db = PostLike(**post_like.model_dump())
    db.add(post_like_db)
    db.commit()
    db.refresh(post_like_db)
    return post_like_db

@post_like_router.get('/', response_model=List[PostLikeOutSchema], summary='Get all posts likes.', tags=['PostLike'])
async def posts_likes(db: Session = Depends(get_db)):
    post_likes_db = db.query(PostLike).all()
    if not post_likes_db:
        raise HTTPException(status_code=404, detail='No posts likes yet.')
    return post_likes_db

@post_like_router.get('/{post_like_id}/', response_model=PostLikeOutSchema, summary='Get posts like by id.', tags=['PostLike'])
async def posts_like_detail(post_like_id: int, db: Session = Depends(get_db)):
    post_like_db1 = db.query(PostLike).filter(PostLike.id==post_like_id).first()
    if not post_like_db1:
        raise HTTPException(status_code=404, detail='Posts like not founded by this id.')
    return post_like_db1

@post_like_router.put('/{post_like_id}/', response_model=dict, summary='Update your posts like.', tags=['PostLike'])
async def posts_like_update(post_like_id: int, post: PostLikeInputSchema, db: Session = Depends(get_db)):
    post_like_db2 = db.query(PostLike).filter(PostLike.id==post_like_id).first()
    if not post_like_db2:
        raise HTTPException(status_code=404, detail='Posts like not founded with this id.')
    for key, value in post.model_dump().items():
        setattr(post_like_db2, key, value)
    db.commit()
    db.refresh(post_like_db2)
    return {'detail': 'Posts like has been changed.'}

@post_like_router.delete('/{post_like_id}/', response_model=dict, summary='Delete posts like.', tags=['PostLike'])
async def posts_like_delete(post_like_id: int, db: Session = Depends(get_db)):
    post_like_db3 = db.query(PostLike).filter(PostLike.id==post_like_id).first()
    if not post_like_db3:
        raise HTTPException(status_code=404, detail='Posts like not founded by this id.')
    db.delete(post_like_db3)
    db.commit()
    return {'detail': 'Posts like has been deleted.'}