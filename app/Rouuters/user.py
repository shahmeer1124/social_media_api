from typing import Optional,List
from fastapi import Body, Depends, FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy import null
from .. import schema
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models
from ..database import Session_Local, engine
from sqlalchemy.orm import Session
from .. import utils
from ..database import get_db

router=APIRouter(
    prefix='/users',
    tags=['Users']
)



# Path operation for creating new user and saving its data inside our user table
@router.post('/',response_model=schema.ReturnUser,status_code=status.HTTP_201_CREATED)
def create_user(user:schema.CreateUser,db: Session = Depends(get_db)):
    hashedpassword=utils.getplainpassword(user.password)
    user.password=hashedpassword
    newuser=models.User(**user.dict())
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser.__dict__

#path operation for getting a user based on id
@router.get('/{id}',response_model=schema.ReturnUser)
def get_user(id:int,db: Session = Depends(get_db)): 
    reterieveduser=db.query(models.User).filter(models.User.id==id).first()
    if not reterieveduser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This user doesn't exist")
    return reterieveduser.__dict__
