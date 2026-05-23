from app.database.models import Follow, UserProfile
from app.database.schema import FollowOutSchema, FollowInputSchema
from app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter, status

follow_router = APIRouter(prefix='/follow')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@follow_router.post('/', response_model=FollowOutSchema,
                    summary='Follow any account', tags=['Follow'])
async def follow_accounts(follow: FollowInputSchema, db: Session = Depends(get_db)):
    follower_user = db.query(UserProfile).filter(UserProfile.id==follow.follower_id).first()
    following_user = db.query(UserProfile).filter(UserProfile.id==follow.following_id).first()
    following_exists = db.query(Follow).filter(
        Follow.follower_id==follow.follower_id,
        Follow.following_id==follow.following_id
    ).first()
    if not follower_user or not following_user:
        raise HTTPException(detail=f'No user with id {follow.follower_id} or {follow.following_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    if following_exists:
        raise HTTPException(detail='U are already following this user', status_code=status.HTTP_409_CONFLICT)
    if follow.follower_id == follow.following_id:
        raise HTTPException(detail='U cannot follow urself', status_code=status.HTTP_400_BAD_REQUEST)
    follow_db = Follow(**follow.model_dump())
    db.add(follow_db)
    db.commit()
    db.refresh(follow_db)
    return follow_db

@follow_router.get('/{user_id}/followers', response_model=List[FollowOutSchema],
                   summary="Get user's followers", tags=['Follow'])
async def get_followers(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} doesnt have followers")
    followers_db = db.query(Follow).filter(Follow.following_id==user_id).limit(20).offset(0).all()
    return followers_db

@follow_router.get('/{user_id}/followings', response_model=List[FollowOutSchema],
                   summary="Get accounts the user follows", tags=['Follow'])
async def get_following(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_id} doesnt have followings")
    followings_db = db.query(Follow).filter(Follow.follower_id==user_id).limit(20).offset(0).all()
    return followings_db

@follow_router.get('/{following_id}/', response_model=FollowOutSchema,
                   summary='Get following by id', tags=['Follow'])
async def following_detail(following_id: int, db: Session = Depends(get_db)):
    following_db1 = db.query(Follow).filter(Follow.id==following_id).first()
    if not following_db1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with id {following_id}')
    return following_db1

@follow_router.delete('/{following_id}/', response_model=dict,
                      summary='Delete following', tags=['Follow'])
async def following_delete(following_id: int, db: Session = Depends(get_db)):
    following_db3 = db.query(Follow).filter(Follow.id==following_id).first()
    if not following_db3:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Following not founded by this id')
    db.delete(following_db3)
    db.commit()
    return {'detail': 'Following has been deleted'}