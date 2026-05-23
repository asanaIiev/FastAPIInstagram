from app.database.models import Follow
from app.database.schema import FollowOutSchema, FollowInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

follow_router = APIRouter(prefix='/follow')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@follow_router.post('/', response_model=FollowOutSchema, summary='Follow any account.', tags=['Follow'])
async def follow_accounts(follow: FollowInputSchema, db: Session = Depends(get_db)):
    following_db = Follow(**follow.model_dump())
    db.add(following_db)
    db.commit()
    db.refresh(following_db)
    return following_db

@follow_router.get('/', response_model=List[FollowOutSchema], summary='Get all followings.', tags=['Follow'])
async def followings_list(db: Session = Depends(get_db)):
    followings_db = db.query(Follow).all()
    if not followings_db:
        raise HTTPException(status_code=404, detail='No followings yet.')
    return followings_db

@follow_router.get('/{following_id}/', response_model=FollowOutSchema, summary='Get following by id.', tags=['Follow'])
async def following_detail(following_id: int, db: Session = Depends(get_db)):
    following_db1 = db.query(Follow).filter(Follow.id==following_id).first()
    if not following_db1:
        raise HTTPException(status_code=404, detail='Following not founded by this id.')
    return following_db1

@follow_router.put('/{following_id}/', response_model=dict, summary='Update your following.', tags=['Follow'])
async def following_update(following_id: int, following: FollowInputSchema, db: Session = Depends(get_db)):
    following_db2 = db.query(Follow).filter(Follow.id==following_id).first()
    if not following_db2:
        raise HTTPException(status_code=404, detail='Following not founded with this id.')
    for key, value in following.model_dump().items():
        setattr(following_db2, key, value)
    db.commit()
    db.refresh(following_db2)
    return {'detail': 'Follow has been changed.'}

@follow_router.delete('/{following_id}/', response_model=dict, summary='Delete following.', tags=['Follow'])
async def following_delete(following_id: int, db: Session = Depends(get_db)):
    following_db3 = db.query(Follow).filter(Follow.id==following_id).first()
    if not following_db3:
        raise HTTPException(status_code=404, detail='Following not founded by this id.')
    db.delete(following_db3)
    db.commit()
    return {'detail': 'Following has been deleted.'}