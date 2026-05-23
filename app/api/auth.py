from app.database.db import SessionLocal
from app.database.models import UserProfile, UserProfileRefresh
from app.database.schema import UserProfileLoginSchema, UserProfileInputSchema, UserProfileOutSchema
from fastapi import HTTPException, APIRouter, Depends, status
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expiration_time = datetime.now(timezone.utc) + expires_delta
    else:
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({'exp': expiration_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))

@auth_router.post('/register', response_model=UserProfileOutSchema, tags=['Auth'])
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    username_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email==user.email).first()
    if username_db or email_db:
        raise HTTPException(detail='This username or email already exists', status_code=status.HTTP_409_CONFLICT)
    user_data = user.model_dump()
    user_data['password'] = get_password_hash(user.password)
    user_db = UserProfile(**user_data)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@auth_router.post('/login', response_model=dict, tags=['Auth'])
async def login(user: UserProfileLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='Invalid credentials', status_code=status.HTTP_400_BAD_REQUEST)
    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})
    token_db = UserProfileRefresh(user_id=user_db.id, refresh_token=refresh_token)
    db.add(token_db)
    db.commit()
    return {
        'access': access_token,
        'refresh': refresh_token,
        'token_type': 'Bearer'
    }

@auth_router.post('/logout', response_model=dict, tags=['Auth'])
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    refresh_db = db.query(UserProfileRefresh).filter(
        UserProfileRefresh.refresh_token==refresh_token
    ).first()
    if not refresh_db:
        raise HTTPException(detail='Invalid token', status_code=status.HTTP_400_BAD_REQUEST)
    db.delete(refresh_db)
    db.commit()
    return {'detail': 'Successfully logged out'}

@auth_router.post('/access', response_model=dict, tags=['Auth'])
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    refresh_db = db.query(UserProfileRefresh).filter(
        UserProfileRefresh.refresh_token==refresh_token
    ).first()
    if not refresh_db:
        raise HTTPException(detail='Invalid token', status_code=status.HTTP_409_CONFLICT)
    access_token = create_access_token({'sub': refresh_db.user_id})
    return {
        'access': access_token,
        'token_type': 'Bearer'
    }