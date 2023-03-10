from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String,ForeignKey
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship




class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published=Column(Boolean,server_default="TRUE",nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=func.now())   
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    
    owner=relationship("User")
    


class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)    
    password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=func.now())
    

class Votes(Base):
    __tablename__='votes'
    post_id=Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)





















# class Pepsi(Base):
#     __tablename__='pepsi'
#     id=Column(Integer,primary_key=True,nullable=False)
#     email=Column(String,nullable=False,unique=True)    
#     password=Column(String,nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=func.now())      