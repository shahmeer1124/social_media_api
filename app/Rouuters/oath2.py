from jose import JWTError,jwt
from datetime import datetime, timedelta
from .. import schema,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..config import setting

oauth2_scheme=OAuth2PasswordBearer('/login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode=data.copy()
# expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    time=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":time})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)  
        id:str=payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data= schema.TokenData(id=id)  
        return token_data   
    except JWTError:
        raise credential_exception


def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to verify credentials",headers={'WWW.Authenticate':"bearer"})
   
    token= verify_access_token(token=token,credential_exception=credential_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user
