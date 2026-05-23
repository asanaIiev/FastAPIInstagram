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
    user_db = db.query(UserProfile).filter(UserProfile.id==comment_like.user_id)
    if not user_db:
        raise HTTPException(detail=f'No user with id {comment_like.user_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    post_db = db.query(Comment).filter(Comment.id==comment_like.comment_id)
    if not post_db:
        raise HTTPException(detail=f'No comment with id {comment_like.comment_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    comment_like_db = CommentLike(**comment_like.model_dump())
    db.add(comment_like_db)
    db.commit()
    db.refresh(comment_like_db)
    return comment_like_db

@comment_like_router.get('/', response_model=List[CommentLikeOutSchema], summary='Get all comments likes', tags=['CommentLike'])
async def comment_like_list(comment_id: int, db: Session = Depends(get_db)):
    return db.query(CommentLike).filter(CommentLike.comment_id==comment_id).all()

@comment_like_router.delete('/{comment_id}/', response_model=dict, summary='Delete comments like', tags=['CommentLike'])
async def comment_like_delete(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(
        CommentLike.user_id==user_id,
        CommentLike.comment_id==comment_id
    ).first()
    if not comment_like_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No likes on this comment by this user')
    db.delete(comment_like_db)
    db.commit()
    return {'detail': 'Comments like has been deleted'}