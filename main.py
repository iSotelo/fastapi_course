from fastapi import FastAPI
from app.routers import user, auth
from app.db.database import Base, engine

# Database configuration
# def create_tables():
#     Base.metadata.create_all(bind=engine)
# create_tables()

# import uvicorn
app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)

# ruta GET
@app.get("/ruta1")
def ruta1():
    """
    Ejemplo de una ruta X
    """
    return {"mensaje": "Bienvenido a mi primer API"}

# if __name__=="__main__":
#     uvicorn.run("main:app",port=8000)