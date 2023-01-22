

from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from typing import List

# Model according to which some one can post
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    # rating:Optional[int]=None


class Create_post(BaseModel):
    title:str
    content:str
    published:bool=True


class UpdatePost(BaseModel):
    title:str
    content:str
    published:bool

# class ReturnUser(BaseModel):
#     email:EmailStr
#     id:int
#     created_at:datetime

#     class config:
#         orm_mode=True 


class ReturnUser(BaseModel):
    email: str
    id: int
    created_at: datetime        
    
class ReturnPost(BaseModel):
    title:str
    content:str
    published:bool
    owner_id:int

    
    class config:
        orm_mode=True  







# class GetAllPost(BaseModel):
#     title:str
#     content:str
#     published:bool=True
#     owner_id:int
#     id:int
#     created_at:datetime
#     owner:ReturnUser
   
#     class config:
#         orm_mode=True 



class GetAllPost(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    id: int
    created_at: datetime
    owner: "ReturnUser"
    votes: int
    

class GetAllPostResponse(BaseModel):
    post: List[GetAllPost]

class CreateUser(BaseModel):
    email:EmailStr
    password:str     

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id: Optional[int]=None 



class Vote(BaseModel):
    post_id:int
    vote_dir:int                     