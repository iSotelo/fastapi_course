from app.db.database import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "usuario"
    id = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    correo = Column(String, unique=True)
    creacion_user = Column(DateTime, default=datetime.now,onupdate=datetime.now)
    actualizacion_user = Column(DateTime, default=datetime.now,onupdate=datetime.now)
    estado = Column(Boolean, default=False)
    username = Column(String)
    password = Column(String)
    venta = relationship("Venta",backref="usuario",cascade="delete,merge")

class Venta(Base):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    venta = Column(Integer)
    ventas_productos = Column(Integer)