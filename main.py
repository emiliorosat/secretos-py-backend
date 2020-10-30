from fastapi import FastAPI, Request, openapi, Header, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID, uuid4
from models import User, Secret, UserAccess, UserIdentity
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, date
import userController
import db

app = FastAPI(
    title="Api Vaul de Secretos",
    version="1.0",
    docs_url="/", 
    redoc_url=None
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://localhost",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

#Usuarios
@app.post("/api/users/register", tags=["users"])
def userRegister(user: UserAccess ):
    return userController.addNewUser(user)

@app.post("/api/users/login", tags=["users"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.User.select().where(db.User.UserName == form_data.username).get()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if(userController.decodePassword(form_data.password, user.Password)):
        token = userController.buildToken(
            UserIdentity(
                Id=user.Id, 
                Email=user.Email, 
                UserName=user.UserName, 
                FullName=user.FullName,
                Disabled=user.Disabled
                ))
        print(token)
        return {"access_token": token, "token_type": "bearer"}
    else: 
        print("No Coinciden las Password")
        return HTTPException(status_code=400, detail="Incorrect username or password")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = userController.checkToken(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user["user"]["Disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user["user"]

@app.get("/api/users/me", tags=["users"])
def getUser( currentUser: User = Depends(get_current_active_user) ):
    userInDb = db.User.select().where(db.User.Id == currentUser["Id"]).get()
    return UserIdentity(Id=userInDb.Id, UserName = userInDb.UserName, Email=userInDb.Email, FullName=userInDb.FullName, Disabled=userInDb.Disabled)

async def IsValidToken(user: User = Depends(get_current_user)):
    now = datetime.now().timestamp()
    leftTime = user["exp"]
    leftTime -= now
    if leftTime >= 0:
        return { "user": user["user"], "status": True }
    else:
        return { "user": None, "status": False }


@app.put("/api/users/update", tags=["users"])
def userUpdate(user: User, isValid = Depends(IsValidToken)):
    if isValid["status"]:
        userInDb = db.User.select().where(db.User.Id == isValid["user"]["Id"]).get()
        userUpdated = 0
        if userInDb.Email != user.Email and userInDb.FullName != user.FullName:
            userUpdated = (db.User.update(Email=user.Email, FullName=user.FullName ).where(db.User.Id == userInDb.Id).execute() )
        elif userInDb.FullName != user.FullName:
            userUpdated = ( db.User.update(FullName=user.FullName).where(db.User.Id == userInDb.Id).execute() )
        elif userInDb.Email != user.Email:
            userUpdated = (db.User.update(Email=user.Email).where(db.User.Id == userInDb.Id).execute() )
        if userUpdated == 1:
            return {"status": True, "message": "User Updated"}
        else:
            return {"status": True, "message": "User No Updated"}
    return {"status": False}

@app.put("/api/users/password", tags=["users"])
def userPasswordUpdate(user: UserAccess, token = Depends(IsValidToken)):
    if token["status"]:
        userInDb = db.User.select().where(db.User.UserName == token["user"]["UserName"]).get()

        same = userController.decodePassword(user.OldPassword, userInDb.Password)
        if same:
            newPswHased = userController.encodePassword(user.OldPassword)
            passUpdated = ( db.User.update(Password=newPswHased).where(db.User.Id == userInDb.Id).execute() )
            if passUpdated == 1:
                return {"status": True, "message": "Password Updated"}
            else:
                return {"status": True, "message": "Password No Updated"}
        else:
            return {"status": True, "message": "Password No Updated"}
    return {"status": False}


@app.get("/api/users/logout", tags=["users"])
def userLogout(token: str = Depends(oauth2_scheme)):
    ok = db.TokenDisabled.create(Token = token, Date = datetime.now())
    ok.save()
    return 


#Secretos
@app.get("/api/secrets", tags=["secrets"])
def GetAllSecrets(token = Depends(IsValidToken)):
    if token["status"]:
        allSecrets = db.Secret().select().filter(db.Secret.UserId == token["user"]["Id"] ).dicts()

        if allSecrets:
            return tuple(allSecrets)
        else:
            return {"message": "No hay Secretos Registrados"}
    return {"message": "Usuario No Valido"}

@app.post("/api/secrets", tags=["secrets"])
def addSecret(secret: Secret, token = Depends(IsValidToken)):
    if token["status"]:
        newSecret = db.Secret.create(
            Id=uuid4(),
            UserId=token["user"]["Id"],
            Titulo=secret.Titulo,
            Description=secret.Description,
            Value=secret.Value,
            Date=secret.Date,
            Place=secret.Place,
            Lat=secret.Lat,
            Lng=secret.Lng
            )
        newSecret.save()
        return {"message": "Secreto Creado Con Exito"}
    return {"message": "Usuario No Valido"}

@app.delete("/api/secrets/{id}", tags=["secrets"])
def secretDelete(id: UUID, token = Depends(IsValidToken)):
    if token["status"]:
        db.Secret.delete().where(db.Secret.Id == id).execute()
        return {"message": "Secreto Eliminado Con Exito"}
    return {"message": "Usuario No Valido"}
    
