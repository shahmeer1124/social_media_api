from passlib.context import CryptContext #this line is added in first step in password hashing after installion of libraries pip install passlib[bcrypt]
# for password hashing this line is added in second step
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getplainpassword(password):
    hasedpassword=pwd_context.hash(password)
    return hasedpassword

def verifypassword(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)    