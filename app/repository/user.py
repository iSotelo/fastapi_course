from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime
from fastapi import HTTPException, status
from app.hashing import Hash


def crear_usuario(usuario, db:Session):
    usuario = usuario.dict()
    try:
        nuevo_usuario = models.User(
            username = usuario["username"],
            password = Hash.hash_password(usuario["password"]),
            nombre = usuario["nombre"],
            apellido = usuario["apellido"],
            direccion = usuario["direccion"],
            telefono = usuario["telefono"],
            creacion_user = datetime.now(),
            actualizacion_user = datetime.now(),
            correo = usuario["correo"],
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail=f"Error creando el usuario {e}"
        )

def obtener_usuarios(db:Session):
    data = db.query(models.User).all()
    return data

def obtener_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el ID {user_id}"
        )
    return usuario

def eliminar_usuario(user_id, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el ID {user_id}"
        )
    try:
        usuario.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail=f"Error eliminando el usuario {e}"
        )
    return {"response": f"Se elimino el usuario con el ID: {user_id}"}

def actualizar_usuario(user_id, update_user, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el ID {user_id}"
        )
    try:
        usuario.update(update_user.dict(exclude_unset=True))
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail=f"Error actualizando el usuario {e}"
        )
    return {"response": f"Se actualizo el usuario ID[{user_id}] correctamente"}