from app.database.db import SessionLocal
from app.database.models import UserProfile
from app.database.schema import UserProfileInputSchema, UserProfileOutSchema
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session

user_router = APIRouter(prefix='/users')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get('/{user_id}/', response_model=UserProfileOutSchema, summary='Get user by id', tags=['Users'])
async def get(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail=f'No user with id {user_id}', status_code=status.HTTP_404_NOT_FOUND)
    return user_db

@user_router.put('/{user_id}/', response_model=UserProfileOutSchema, summary='Change user credentials', tags=['Users'])
async def put(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail=f'No user with id {user_id}', status_code=status.HTTP_404_NOT_FOUND)
    update_user = user.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.delete('/{user_id}/', response_model=dict, summary='Delete account', tags=['Users'])
async def delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db: raise HTTPException(detail=f'No user with id {user_id}', status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user_db)
    db.commit()
    return {'detail': 'User has been deleted'}