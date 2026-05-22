from fast_insta.database.db import SessionLocal
from fast_insta.database.models import UserProfile
from fast_insta.database.schema import UserProfileInputSchema, UserProfileOutSchema
from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

user_router = APIRouter(prefix='/users')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema, tags=['Users'])
async def post(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    if user: raise HTTPException(detail='This username or email already exists', status_code=400)
    user_db = UserProfile(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema], summary='Get all users', tags=['Users'])
async def get(db: Session = Depends(get_db)):
    users_db = db.query(UserProfile).all()
    if not users_db: raise HTTPException(detail='No users', status_code=status.HTTP_404_NOT_FOUND)
    return users_db

@user_router.get('/{user_id}/', response_model=UserProfileOutSchema, summary='Get users by id', tags=['Users'])
async def get(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail='No user', status_code=status.HTTP_404_NOT_FOUND)
    return user_db

@user_router.put('/{user_id}/', response_model=UserProfileOutSchema, summary='Change users credentials', tags=['Users'])
async def put(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail='No user with this id', status_code=status.HTTP_404_NOT_FOUND)
    update_user = user.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.delete('/{user_id}/', response_model=dict, summary='Delete user', tags=['Users'])
async def delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail='No user with this id', status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user_db)
    db.commit()
    return {'detail': 'User has been deleted'}