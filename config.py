from os import access
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv



class Settings(BaseSettings):  
   database_hostname: str = "localhost"
   database_port: str = "5432"  
   database_password: str = "cheetohan1%40"
   database_name: str = "postgres"
   database_username: str = "postgres"
   secret_key: str = "your_secret_key"  # Change this to your actual secret key
   algorithm: str = "HS256" 
   access_token_expire_minutes: int = 30 
   
   class Config:
       env_file = ".env"
     

settings = Settings() 