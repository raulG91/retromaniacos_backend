from pydantic import BaseModel,Field,EmailStr
from datetime import date, datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field as sqlmodel_Field, Session, select
from ..util import hash_password

class ExecutivePosition(str,Enum):
  PRESIDENT = "President"
  VICE_PRESIDENT = "Vice President"
  TREASURER = "Treasurer"
  OTHER = "Other"


class UserModel(BaseModel):
  name: str = Field(description="First name")
  lastName: str = Field(description="Last name")
  secondLastName: str | None = Field(default=None, description="Second last name")
  dateOfBirth: date = Field(description="Date of birth")
  nationalId: str = Field(description="National identification number",min_length=9,max_length=12)
  executivePosition: ExecutivePosition | None = Field(default=None, description="Executive position held by the user, if any")
  email: EmailStr = Field(description="Email address")
  phone: str = Field(description="Phone number",pattern=r'^[6,7,8,9]\d{8}$')

class UserIn(UserModel):
  password: str = Field(description="Password",min_length=8,max_length=64)

class UserOut(UserModel):
    id: int = Field(description="User ID")

class User(SQLModel, table=True):
    id: int | None = sqlmodel_Field(default=None, primary_key=True)
    name: str
    lastName: str
    secondLastName: str | None = sqlmodel_Field(default=None)
    dateOfBirth: date
    nationalId: str
    executivePosition: str | None = sqlmodel_Field(default=None)
    email: str = sqlmodel_Field(index=True, unique=True)
    phone:str
    hashPassword: str
    active: bool = sqlmodel_Field(default=True)
    creationDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModifiedDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
class PasswordUpdate(BaseModel):
    password: str = Field(description="New password", min_length=8, max_length=64)
users:list[UserOut] = []
class UserService:
  @staticmethod
  def get_users() -> list[UserOut]:
      return users
  @staticmethod
  def createUser(user:UserIn, session: Session) -> User:
        
        statement = select(User).where(User.email == user.email)
        try:
          user_exist = session.exec(statement).first()
        except Exception as e:
          raise Exception(f"Error checking user existence: {str(e)}")
        if not user_exist:
            try:
              userDB = User(
                  name=user.name.lower(),
                  lastName=user.lastName.lower(),
                  secondLastName=user.secondLastName.lower() if user.secondLastName else None,
                  dateOfBirth=user.dateOfBirth,
                  nationalId=user.nationalId,
                  executivePosition=user.executivePosition.value if user.executivePosition else None,
                  email=user.email,
                  phone=user.phone,
                  hashPassword=hash_password(user.password),
                  active=True,
                  lastModifiedDate= datetime.now(timezone.utc)
              )
              session.add(userDB)
              session.commit()
              session.refresh(userDB)
              return userDB
            except Exception as e:
              session.rollback()
              raise Exception(f"Error updating user: {str(e)}")  
        else:
           raise ValueError("User already exist")  
  @staticmethod
  def update_user(id:int,updated_user:UserIn,session:Session) -> User:
     statement = select(User).where(User.id == id)
     try:
        user = session.exec(statement).first()
        if user:
            user.name = updated_user.name.lower()
            user.lastName = updated_user.lastName.lower()
            user.secondLastName = updated_user.secondLastName.lower() if updated_user.secondLastName else None
            user.dateOfBirth = updated_user.dateOfBirth
            user.nationalId = updated_user.nationalId
            user.email = updated_user.email
            user.phone = updated_user.phone
            user.executivePosition = updated_user.executivePosition.value if updated_user.executivePosition else None
            user.lastModifiedDate = datetime.now(timezone.utc)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
           
     except Exception as e:
          raise Exception(f"Error checking user existence: {str(e)}")
  @staticmethod
  def delete_user(id:int,session:Session) -> None:
    statement = select(User).where(User.id == id)
    try:
        user = session.exec(statement).first()
        if user:
          user.active = False
          user.lastModifiedDate = datetime.now(timezone.utc)
          session.add(user)
          session.commit()
          session.refresh(user)
        else:
          raise ValueError("User doesn't exist")   
    except Exception as e:
       raise Exception(f"Error deleting user: {str(e)}")   
  @staticmethod
  def update_user_password(id:int, new_password:str, session:Session) -> User:
     statement = select(User).where(User.id == id)
     try:
        user = session.exec(statement).first()
        if user:
          user.hashPassword = hash_password(new_password)
          user.lastModifiedDate = datetime.now(timezone.utc)
          session.add(user)
          session.commit()
          session.refresh(user)
          return user
        else:
          raise ValueError("User doesn't exist")   
     except Exception as e:
       raise Exception(f"Error updating user password: {str(e)}")
  @staticmethod
  def get_user_by_email(email:str,session:Session ) -> User | None:
     statement = select(User).where(User.email == email)
     try:
        user = session.exec(statement).first()
        if user:
           return user
        else:
          return None
     except Exception as e:
        raise Exception(f"Error retrieving user: {str(e)}")   
  @staticmethod
  def get_users() -> list[UserOut]:
         return users