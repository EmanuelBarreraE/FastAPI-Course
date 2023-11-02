from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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

#------------Create a Post------------#
class PostCreate(PostBase):
    pass
#-------------------------------------#

#------------Create the response scheme------------#
class Post(PostBase):
    id: int
    created_at: datetime
    
    #Orm_mode -> por que se usa
    class Config:
        orm_mode = True
#---------------------------------------------------#

#------------Create a UserBase scheme------------#
class UserCreate(BaseModel):
    email: EmailStr
    password: str
#------------------------------------------------#
 
#------------Create a UserResponse scheme------------#
class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
#----------------------------------------------------#

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
