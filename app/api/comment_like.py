from app.database.models import CommentLike, UserProfile, Comment
from app.database.schema import CommentLikeOutSchema, CommentLikeInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter, status

comment_like_router = APIRouter(prefix='/comment_like')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_like_router.post('/', response_model=CommentLikeOutSchema, summary='Like the comment', tags=['CommentLike'])
async def like_comment(comment_like: CommentLikeInputSchema, db: Session = Depends(get_db)):
    comment_like_user = db.query(UserProfile).filter(UserProfile.id==comment_like.user_id)
    comment_like_comment = db.query(Comment).filter(Comment.id==comment_like.comment_id)
    if not comment_like_user:
        raise HTTPException(detail=f'No user with id {comment_like.user_id}', status_code=status.HTTP_404_NOT_FOUND)
    if not comment_like_comment:
        raise HTTPException(detail=f'No comment with id {comment_like.comment_id}')
    comment_like_db = CommentLike(**comment_like.model_dump())
    db.add(comment_like_db)
    db.commit()
    db.refresh(comment_like_db)
    return comment_like_db

@comment_like_router.get('/', response_model=List[CommentLikeOutSchema], summary='Get all comments likes', tags=['CommentLike'])
async def comment_like_list(db: Session = Depends(get_db)):
    comment_likes_db = db.query(CommentLike).all()
    if not comment_likes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comments doesnt have likes yet')
    return comment_likes_db

@comment_like_router.get('/{comment_like_id}/', response_model=CommentLikeOutSchema, summary='Get comments like by id', tags=['CommentLike'])
async def comment_like_detail(comment_like_id: int, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(CommentLike.id==comment_like_id).first()
    if not comment_like_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comments like not founded by this id')
    return comment_like_db

@comment_like_router.delete('/{comment_like_id}/', response_model=dict, summary='Delete comments like', tags=['CommentLike'])
async def comment_like_delete(comment_like_id: int, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(CommentLike.id==comment_like_id).first()
    if not comment_like_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No comments like with id {comment_like_id}')
    db.delete(comment_like_db)
    db.commit()
    return {'detail': 'Comments like has been deleted'}