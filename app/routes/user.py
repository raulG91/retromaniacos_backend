from fastapi import APIRouter,status,Body, HTTPException, Depends
from ..models.user import UserIn,UserOut,UserService, User, PasswordUpdate, UserModel
from ..models.token import Token
from typing import Annotated
from ..db import SessionDep
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm;
from ..util import verify_password
from datetime import datetime, timedelta,timezone
import jwt
from jwt.exceptions import InvalidTokenError
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
userRouter = APIRouter(tags=["User"],prefix="/api")

#Define endpoint to get token
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

def get_current_user(token: Annotated[str,Depends(oauth2_schema)],session: SessionDep) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #Get username
        username = payload.get("sub",None)
        if username is None:
            raise credentials_exception
        else:
            #Check if token has expired
            exp = payload.get("exp", None)
            if exp is None or datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
                raise credentials_exception


    except InvalidTokenError:
        raise credentials_exception
        
    user = UserService.get_user_by_email(username,session)
    if user:
        return user
    else:
        raise credentials_exception
    
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)])->UserOut:
    if current_user.active:
        return UserOut(**current_user.model_dump())
    else:
        raise HTTPException(status_code=400, detail="Inactive user")

@userRouter.get("/users", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users()->list[UserOut]:
    return UserService.get_users()

@userRouter.post("/user",status_code=status.HTTP_201_CREATED,response_model=UserOut)
async def create_user(user: Annotated[UserIn, Body()],session: SessionDep) -> UserOut:
    try:
        user = UserService.createUser(user,session)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
@userRouter.get("/user/me", response_model=UserOut,description="Get current user data")
async def get_current_user_data(current_user: Annotated[UserOut, Depends(get_current_active_user)]) -> UserOut : 
    return current_user

@userRouter.put("/user/me", response_model=UserOut, description="Update current user data")
async def update_current_user_data(updated_user: Annotated[UserModel, Body()], current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> UserOut:
    try:
        user = UserService.update_user(current_user.id, updated_user, session)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating user")
#Update user password
@userRouter.patch("/user/me/password", status_code=status.HTTP_200_OK, description="Update current user password")    
async def update_current_user_password(new_password: Annotated[PasswordUpdate, Body()], current_user: Annotated[UserOut, Depends(get_current_active_user)],session: SessionDep) -> UserOut:
    try:
        user = UserService.update_user_password(current_user.id, new_password.password, session)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating user password")
#Delete current user    
@userRouter.delete("/user/me", status_code=status.HTTP_204_NO_CONTENT, description="Delete current user")
async def delete_current_user(current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep):
    try:
        UserService.delete_user(current_user.id, session)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting user")

#Get authentication token    
@userRouter.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
   #Autheticate user with the provided credentials
   user = authenticate_user(form_data.username, form_data.password, session)
   if user:
        access_token = create_access_token(user.email)
        return Token(access_token=access_token, token_type="bearer")
   else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                           detail="Incorrect username or password",
                           headers={"WWW-Authenticate": "Bearer"})

def authenticate_user(email: str, password: str, session: SessionDep) -> User | None:
    user = UserService.get_user_by_email(email, session)
    if user and user.active and verify_password(password, user.hashPassword):
        return user
    return None

def create_access_token(username: str)->str:
    payload = {"sub": username,
               "exp": datetime.now(timezone.utc)  + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


