from app.database.models import Post, UserProfile
from app.database.schema import PostOutSchema, PostInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter, status

post_router = APIRouter(prefix='/post')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_router.post('/', response_model=PostOutSchema, summary='Create post', tags=['Post'])
async def create_post(post: PostInputSchema, db: Session = Depends(get_db)):
    post_user = db.query(UserProfile).filter(UserProfile.id==post.user_id).first()
    if not post_user:
        raise HTTPException(detail=f'No user with id {post.user_id}', status_code=status.HTTP_404_NOT_FOUND)
    post_db = Post(**post.model_dump())
    db.add(post_db)
    db.commit()
    db.refresh(post_db)
    return post_db

@post_router.get('/', response_model=List[PostOutSchema], summary='Get all posts', tags=['Post'])
async def post_list(db: Session = Depends(get_db)):
    posts_db = db.query(Post).all()
    if not posts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No posts yet')
    return posts_db

@post_router.get('/{post_id}/', response_model=PostOutSchema, summary='Get post by id', tags=['Post'])
async def post_detail(post_id: int, db: Session = Depends(get_db)):
    post_db = db.query(Post).filter(Post.id==post_id).first()
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post with id {post_id}')
    return post_db

@post_router.put('/{post_id}/', response_model=PostOutSchema, summary='Update your post', tags=['Post'])
async def post_update(post_id: int, post: PostInputSchema, db: Session = Depends(get_db)):
    post_user = db.query(UserProfile).filter(UserProfile.id==post.user_id).first()
    if not post_user:
        raise HTTPException(detail=f'No user with id {post.user_id}', status_code=status.HTTP_404_NOT_FOUND)
    post_db = db.query(Post).filter(Post.id==post_id).first()
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post with id {post_id}')
    update_post = post.model_dump(exclude_unset=True)
    for key, value in update_post.items():
        setattr(post_db, key, value)
    db.commit()
    db.refresh(post_db)
    return post_db

@post_router.delete('/{post_id}/', response_model=dict, summary='Delete post', tags=['Post'])
async def post_delete(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post_db = db.query(Post).filter(
        Post.post_user==user_id,
        Post.id==post_id
    ).first()
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user on this post')
    db.delete(post_db)
    db.commit()
    return {'detail': 'Post has been deleted'}