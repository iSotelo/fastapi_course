from fastapi.testclient import TestClient
import sys, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

# actualizamos la url del sistema, para 
# obtener la app desde main
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db

db_path = os.path.join(os.path.dirname(__file__),'test.db')
db_uri = "sqlite:///{}".format(db_path)
SQLALQUEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALQUEMY_DATABASE_URL, connect_args={"check_same_thread":False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False,autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def insertar_usuario_prueba():
    password_hash = Hash.hash_password("mipawd123.")
    engine_test.execute(
        f""" 
        INSERT INTO usuario(nombre, apellido, direccion, correo, telefono, username, password, creacion_user, actualizacion_user)
        VALUES
        ("jesus", "salas", "c. hidalgo", "jesus@hotmail.com", 3214, "josh", "{password_hash}", "{datetime.now()}", "{datetime.now()}")
        """
    )
insertar_usuario_prueba()


def test_crear_usuario():
    time.sleep(2)
    usuario = {
        "nombre": "jose isaias",
        "apellido": "sotelo",
        "direccion": "alameda",
        "telefono": 3215,
        "correo": "sotelo1@gmail.com",
        "creacion_user": "2022-07-20T00:37:16.716928",
        "actualizacion_user": "2022-07-20T00:37:16.716928",
        "estado": True,
        "username": "sotelo",
        "password": "123."
    }
    
    response = cliente.post("/user/", json=usuario)
    ## para cuando el usuario no esta logeado
    assert response.status_code == 401
    
    ## generamos el login del usuario
    usuario_login = {
        "username":"josh",
        "password":"mipawd123."
    }
    
    response_token = cliente.post("/login/", data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    
    headers = { "Authorization": f"Bearer {response_token.json()['access_token']}" }
    response = cliente.post("/user/", json=usuario, headers=headers)
    assert response.status_code == 201
    assert response.json()["response"] == "Se agrego con exito el usuario"
    

def test_obtener_usuarios():
    response = cliente.get("/user/")
    assert response.status_code == 401
    
    usuario_login = {
        "username":"josh",
        "password":"mipawd123."
    }
    response_token = cliente.post("/login/", data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    
    headers = { "Authorization": f"Bearer {response_token.json()['access_token']}" }
    response = cliente.get("/user/", headers=headers)
    assert len(response.json()) == 2

def test_obtener_usuario():
    response = cliente.get("/user/1")
    assert response.json()["username"]=="josh"

def test_eliminar_usuario():
    response = cliente.delete("/user/1")
    assert response.json()["response"] == "Se elimino el usuario con el ID: 1"
    response_user = cliente.get("/user/1")
    assert response_user.json()["detail"] == "No existe el usuario con el ID 1"

def test_actualizar_usuario():
    usuario = {
        "username":"jose isaias actualizado"
    }
    
    response = cliente.patch("/user/2", json=usuario)
    # print(response.json())
    assert response.json()["response"] == "Se actualizo el usuario ID[2] correctamente"
    response_user = cliente.get("/user/2")
    # print(response_user.json())
    assert response_user.json()["username"] == usuario["username"]

def test_no_encuentra_usuario():
    usuario = {
        "username":"jose isaias actualizado"
    }
    
    response = cliente.patch("/user/12", json=usuario)
    # print(response.json())
    assert response.json()["detail"] == "No existe el usuario con el ID 12"

# este se ejecutara como un test
def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    os.remove(db_path)