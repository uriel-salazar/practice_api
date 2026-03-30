from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ This class inherited from
    Base Settings load values from .env file

    """
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    secret_key:SecretStr
    algorithm:str ="HS256"
    database_url:str
    # Converts env variable from string to int. 
    access_token_expires_minutes:int = 30
    
settings=Settings() #type:ignore
    