from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional
from datetime import date

class StatusChoices(str, Enum):
    SIMPLE = 'Simple'
    PRO = 'Pro'

class UserProfileLoginSchema(BaseModel):
    username: str
    password: str

class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: StatusChoices
    data_registered: date
class UserProfileInputSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)
    email: EmailStr
    status: StatusChoices

class FollowOutSchema(BaseModel):
    id: int
    follower_id: int
    following_id: int
    followed_date: date
class FollowInputSchema(BaseModel):
    follower_id: int
    following_id: int

class PostOutSchema(BaseModel):
    id: int
    user_id: int
    post: str
    description: str
    hashtag: str
    created_date: date
class PostInputSchema(BaseModel):
    user_id: int
    post: str
    description: Optional[str] = Field(max_length=100)
    hashtag: Optional[str] = Field(max_length=100)

class PostLikeOutSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    like: bool
class PostLikeInputSchema(BaseModel):
    user_id: int
    post_id: int
    like: bool

class CommentOutSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    comment: str
    created_date: date
class CommentInputSchema(BaseModel):
    user_id: int
    post_id: int
    comment: str = Field(min_length=1, max_length=100)

class CommentLikeOutSchema(BaseModel):
    id: int
    user_id: int
    comment_id: int
    like: bool
class CommentLikeInputSchema(BaseModel):
    user_id: int
    comment_id: int
    like: bool