from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

# Schema de User
class User(BaseModel):
    nombre:str
    apellido: str
    direccion: Optional[str]
    telefono: int
    correo: str
    creacion_user: datetime=datetime.now()
    actualizacion_user: datetime=datetime.now()
    estado: bool
    username: str
    password: str
    
class UpdateUser(BaseModel):
    nombre:str = None
    apellido: str = None
    direccion: str = None
    telefono: int = None
    correo: str = None
    username: str = None
    password: str = None
    # actualizacion_user: datetime=datetime.now()

# schema of UserId
class UserId(BaseModel):
    id: int

# response for 
class ShowUser(BaseModel):
    username:str 
    nombre:str 
    correo:str 
    class Config():
        orm_mode = True

#login schema
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None