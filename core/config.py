import os
from dotenv import load_dotenv
from pathlib import Path

# debemos de localizar el archivo .env en la estructura del proyecto
env_path = Path('.') / '.env'
# pprint(env_path)
# print(env_path)
# cargamos el archivo .env en memoria
load_dotenv(dotenv_path=env_path)
# print(os.getenv('POSTGRES_DB'))
# print(os.getenv('POSTGRES_SERVER'))
# print(os.getenv('POSTGRES_USER'))
# print(os.getenv('POSTGRES_PASSWORD'))
# print(os.getenv('POSTGRES_PORT'))

class Settings():
    PROJECT_NAME:str = "Proyecto Fats API"
    PROJECT_VERSION:str = "0.1.0"
    
    POSTGRES_DB:str = os.getenv('POSTGRES_DB')
    
    POSTGRES_SERVER:str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')
    
    POSTGRES_USER:str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
    
    # url connnection string for postgres database
    # SQLALQUEMY_DATABASE_URL = "postgresql://[user]:[password]@[host]:[port]/[database_name]"
    SQLALQUEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
settings = Settings()