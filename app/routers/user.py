from pyexpat import model
from fastapi import APIRouter, Depends, status
from pprint import pprint
from app.schemas import ShowUser, UpdateUser, User, UserId
from datetime import datetime
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import models
from typing import List
from app.repository import user
from app.oauth import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# usuarios = []

# Usamos response_model para definir el schema de respuesta
@router.get("/", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def obtener_usuarios(db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtiene todos los usuarios registrados
    """
    data = user.obtener_usuarios(db)
    return data

#Ruta POST, pasandole un schema de tipo USER
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario:User, db:Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    """
    Registra un usuario
    """
    # print("Schema USER: ", user)
    # podemos convertir el schema en dict
    # print("Schema User como diccionario: ", user.dict())
    # accede a las propiedades de usuario
    user.crear_usuario(usuario, db)
    return {"response": "Se agrego con exito el usuario"}

@router.get("/{user_id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
def obtener_usuario(user_id: int, db:Session = Depends(get_db)): # Se utilizan los tiping definiendo user_id como int
    """
    Consulta un usuario por su ID.
    NOTA: Si mandamos parametros desde la URL es permitido utilizar el metodo como GET, pero
    cuando mandamos parametros como schema, entonces debemos usar POST.
    """
    usuario = user.obtener_usuario(user_id, db)
    return usuario
    # Codigo para cuando se maneja la lista de usuarios
    # for user in usuarios:
    #     # Cada usuario es de tipo dict, ya que se asi se guardaron desde el EP crear_usuario
    #     if user["id"] == user_id:
    #         return user

# queda como referencia
# @router.post("/obtener_usuario")
# def obtener_usuario_2(user_id: UserId):
#     """
#     Consulta un usuario por su ID usando un schema como parametro.
#     NOTA: Si mandamos parametros desde la URL es permitido utilizar el metodo como GET, pero
#     cuando mandamos parametros como schema, entonces debemos usar POST. Puede confirmar lo 
#     enterior cambiando a GET este EndPoint e intetar un request
#     """
#     for user in usuarios:
#         # Cada usuario es de tipo dict, ya que se asi se guardaron desde el EP crear_usuario
#         if user["id"] == user_id.id:
#             return user
#     return {"response": "Error 404: Usuario no encontrado."}

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id: int, db:Session = Depends(get_db)):
    """
    Permitie eliminar un usuario por su Id
    \n
    NOTA: Este EndPoint al ser de tipo delete no permite el uso de Schema como tal, es decir no se puede \n
    definir de la siguiente manera: \n
        \t def eliminar_usuario(user_id: UserId): \n
    Por lo tanto queda definido así: \n
        \t def eliminar_usuario(user_id: int):
    """
    response = user.eliminar_usuario(user_id, db)
    return response
    
    ## ejemplo recorriendo una lista/array de usuarios
    # for index,user in enumerate(usuarios):
    #     if user["id"] == user_id:
    #         usuarios.pop(index)
    #         return {"response": f"Se elimino el usuario con el ID: {user_id}"}
    # return {"response": "Usuario no encontrado"}

# Este EP no es utilizado solo esta como referencia
# @router.put("/{user_id}")
# def actualizar_usuario(user_id: int, update_user:User):
#     """
#     Permite realiza la actualización de un usuario, mediante su ID y el schema
#     """
#     for index, user in enumerate(usuarios):
#         if user["id"] == user_id:
#             new_user_data = update_user.dict()
#             usuarios[index]["id"] = new_user_data["id"]
#             usuarios[index]["nombre"] = new_user_data["nombre"]
#             usuarios[index]["apellido"] = new_user_data["apellido"]
#             usuarios[index]["telefono"] = new_user_data["telefono"]
#             usuarios[index]["direccion"] = new_user_data["direccion"]
#             usuarios[index]["actualizacion_user"] = datetime.now()
#             return {"response":"Se actualizo el usuario con exito"}
#     return {"response":"Usuario no encontrado"}

@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def actualizar_usuario(user_id: int, update_user:UpdateUser, db:Session = Depends(get_db)):
    """
    Permite realiza la actualización de un usuario, mediante su ID y el schema
    """
    response = user.actualizar_usuario(user_id, update_user, db)
    return response

