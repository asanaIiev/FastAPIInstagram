from app.database.models import Comment
from app.database.schema import CommentOutSchema, CommentInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

comment_router = APIRouter(prefix='/comment')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_router.post('/', response_model=CommentOutSchema, summary='Create comment.', tags=['Comment'])
async def create_comment(comment: CommentInputSchema, db: Session = Depends(get_db)):
    comment_db = Comment(**comment.model_dump())
    db.add(comment_db)
    db.commit()
    db.refresh(comment_db)
    return comment_db

@comment_router.get('/', response_model=List[CommentOutSchema], summary='Get all comments.', tags=['Comment'])
async def comment_list(db: Session = Depends(get_db)):
    comments_db = db.query(Comment).all()
    if not comments_db:
        raise HTTPException(status_code=404, detail='No comments yet.')
    return comments_db

@comment_router.get('/{comment_id}/', response_model=CommentOutSchema, summary='Get comment by id.', tags=['Comment'])
async def comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Comment not founded by this id.')
    return comment_db

@comment_router.put('/{comment_id}/', response_model=dict, summary='Update your comment.', tags=['Comment'])
async def comment_update(comment_id: int, comment: CommentInputSchema, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Comment not founded with this id.')
    for key, value in comment.model_dump().items():
        setattr(comment_db, key, value)
    db.commit()
    db.refresh(comment_db)
    return {'detail': 'Comment has been changed.'}

@comment_router.delete('/{comment_id}/', response_model=dict, summary='Delete comment.', tags=['Comment'])
async def comment_delete(comment_id: int, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id==comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Comment not founded by this id.')
    db.delete(comment_db)
    db.commit()
    return {'detail': 'Comment has been deleted.'}