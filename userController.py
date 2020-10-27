from settings import jwtSecret
import db
from jwt import encode, decode
from datetime import time, datetime
from bcrypt import hashpw, gensalt, checkpw
from models import User, UserAccess, UserIdentity
from uuid import uuid4, UUID


def encodePassword(password: str):
    return hashpw(password.encode("utf-8"), gensalt())

def decodePassword(password: str, hashed: str):
    return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def buildToken(user: UserIdentity):
    now = datetime.now().timestamp()
    timeSession = 30 * 60 * 1000 
    exp = timeSession + now
    
    return encode({"exp": exp, "user": {
        "Id": str( user.Id ),
        "UserName": user.UserName,
        "Email": user.Email,
        "FullName": user.FullName,
        "Disabled": user.Disabled
    }}, jwtSecret)


def checkToken(token: str):
    decoded = decode(token, jwtSecret)
    return decoded

def addNewUser(user: UserAccess):
    psw = user.Password
    PHashed = encodePassword(psw)
    uid = uuid4()
    nUser = db.User.create(
        Id = uid,
        Email=user.Email, 
        UserName=user.UserName,
        FullName=user.FullName, 
        Disabled=False, 
        Password=PHashed
        )
    nUser.save()
    user = db.User.select().where(db.User.UserName == user.UserName).get()
    token = buildToken(
        UserIdentity(
        Id=uid, 
        Email=user.Email, 
        UserName=user.UserName, 
        FullName=user.FullName,
        Disabled=user.Disabled
    ))
    return {"access_token": token, "token_type": "bearer"}
    

def updateUser():
    return

def resetPassword():
    return


def logoutUser():
    return
    