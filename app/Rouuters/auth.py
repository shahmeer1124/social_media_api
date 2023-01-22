from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema import CreateUser
from ..import models,utils
from . import oath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schema


router=APIRouter(
    prefix='/login',
    tags=["Authentication"])

# Path operation for login a user and get the token
@router.post('/',response_model=schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    reteriveduser=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not reteriveduser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.verifypassword(user_credentials.password,reteriveduser.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")  
    # If everything gone well this is the time to create a token
    access_token=oath2.create_access_token(data={"user_id":reteriveduser.id})
    return {"access_token":access_token ,"token_type":"bearer"}
    
      
 
    


