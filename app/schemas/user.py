from datetime import datetime
from enum import IntEnum, Enum
from typing import Optional
from core.database.schema import BaseModel
from app.schemas.profile import CustomerReadOnly, EmployeeReadOnly

class Role(BaseModel):
    id: int 
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    
    class Config:
        orm_mode = True  

class RoleEnum(IntEnum, Enum):
    customer = 1
    employee = 2
 
class AuthUser(User):
    password: str
    role: Optional[RoleEnum] = 1

    class Config:
        orm_mode = True 

class AdminUser(User):
    role: Optional[int] = 1
    password: str
    is_active: Optional[bool] = False

class AdminUpdateUser(BaseModel):
    is_active: bool = False
    role: int = 1
    password: Optional[str]

    class Config:
        orm_mode = True  

class UserProfile(User):
    password: str
     
class UserReadOnly(User):
    id: Optional[int]
    role: Optional[Role]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: Optional[bool] = False


class CustomerProfileReadOnly(UserReadOnly):
    customer: Optional[CustomerReadOnly]

class EmployeeProfileReadOnly(UserReadOnly):
    employee:  Optional[EmployeeReadOnly]