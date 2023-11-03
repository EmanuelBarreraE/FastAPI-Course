from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
#------------Create table posts------------#
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
#------------------------------------------#

#------------Create a PostBase scheme------------#
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
#-------------------------------------#

#------------Create the Post Response------------#
class PostCreate(PostBase):
    pass
#-------------------------------------#

#------------Create a UserResponse scheme------------#
class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
#----------------------------------------------------#

#------------Create the response scheme------------#
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    #Orm_mode -> por que se usa
    class Config:
        orm_mode = True
#---------------------------------------------------#

#------------PostVote scheme------------#
class PostOut(BaseModel):
    Post: Post
    votes: int
#----------------------------------------#


#------------Create a UserBase scheme------------#
class UserCreate(BaseModel):
    email: EmailStr
    password: str
#------------------------------------------------#
 


#------------Login scheme------------#
class UserLogin(BaseModel):
    email: EmailStr
    password: str   
#-------------------------------------#

#------------Token scheme------------#
class Token(BaseModel):
    access_token: str
    token_type: str
#------------------------------------#

#------------TokenData scheme------------#
class TokenData(BaseModel):
    id: Optional[int] = None
#----------------------------------------#

#------------Vote scheme------------#
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
#----------------------------------------#
