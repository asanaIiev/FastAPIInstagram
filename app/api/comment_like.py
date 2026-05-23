from app.database.models import CommentLike
from app.database.schema import CommentLikeOutSchema, CommentLikeInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

comment_like_router = APIRouter(prefix='/comment_like')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_like_router.post('/', response_model=CommentLikeOutSchema, summary='Like the comment.', tags=['CommentLike'])
async def like_comment(comment_like: CommentLikeInputSchema, db: Session = Depends(get_db)):
    comment_like_db = CommentLike(**comment_like.model_dump())
    db.add(comment_like_db)
    db.commit()
    db.refresh(comment_like_db)
    return comment_like_db

@comment_like_router.get('/', response_model=List[CommentLikeOutSchema], summary='Get all comments likes.', tags=['CommentLike'])
async def comment_like_list(db: Session = Depends(get_db)):
    comment_likes_db = db.query(CommentLike).all()
    if not comment_likes_db:
        raise HTTPException(status_code=404, detail='Comment does not have likes yet.')
    return comment_likes_db

@comment_like_router.get('/{comment_like_id}/', response_model=CommentLikeOutSchema, summary='Get comments like by id.', tags=['CommentLike'])
async def comment_like_detail(comment_like_id: int, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(CommentLike.id==comment_like_id).first()
    if not comment_like_db:
        raise HTTPException(status_code=404, detail='Comments like not founded by this id.')
    return comment_like_db

@comment_like_router.put('/{comment_like_id}/', response_model=dict, summary='Update your comments like.', tags=['CommentLike'])
async def comment_like_update(comment_like_id: int, comment_like: CommentLikeOutSchema, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(CommentLike.id==comment_like_id).first()
    if not comment_like_db:
        raise HTTPException(status_code=404, detail='Comments like not founded with this id.')
    for key, value in comment_like.model_dump().items():
        setattr(comment_like_db, key, value)
    db.commit()
    db.refresh(comment_like_db)
    return {'detail': 'Comments like has been changed.'}

@comment_like_router.delete('/{comment_like_id}/', response_model=dict, summary='Delete comments like.', tags=['CommentLike'])
async def comment_like_delete(comment_like_id: int, db: Session = Depends(get_db)):
    comment_like_db = db.query(CommentLike).filter(CommentLike.id==comment_like_id).first()
    if not comment_like_db:
        raise HTTPException(status_code=404, detail='Comments like not founded by this id.')
    db.delete(comment_like_db)
    db.commit()
    return {'detail': 'Comments like has been deleted.'}