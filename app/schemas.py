from re import L
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class JobBase(BaseModel):
    title: str
    user: str
    
class JobCreate(BaseModel):
    name: str
    description: str
    account_id: Optional[int]
    estimated_budget: float

class Jobs(BaseModel):
    id: int
    name: str
    description: str
    account_id: int
    estimated_budget: float
    created_at: datetime

    class Config:
        orm_mode = True





class AccountUpdate(BaseModel):
    email: Optional[EmailStr]
    number: Optional[str]
    is_active: Optional[bool] = True

class AccountCreate(BaseModel):
    email: EmailStr
    number: str
    password: str
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Accounts(BaseModel):
    id: int
    email: EmailStr
    number: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True



class ProfileBase(BaseModel):
    firstname: str
    lastname:str
    gender: str
    country_id: int
    region: str
    city: str
    town: str
    street: str
    dob: str


class CreateProfile(ProfileBase):
    pass

class UpdateProfile(ProfileBase):
    pass

class GetProfile(ProfileBase):
    id: int
    pass

    class Config:
        orm_mode = True


class CreateCountry(BaseModel):
    name: str
    zipcode: Optional[int] = 0


class Country(BaseModel):
    id: int
    name: str
    zipcode: Optional[int] = 0
    account_id: int
    created_at: datetime

    class Config:
        orm_mode = True





class CreateDegree(BaseModel):
    name: str
    account_id: int

class Degree(BaseModel):
    id: int
    name: str
    account_id: int
    created_at: datetime

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
