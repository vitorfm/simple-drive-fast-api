from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    storage_backend: str = "local"
    database_url: str = "sqlite:///./simpledrive.db"
    local_storage_path: str = "./storage"
    api_token: str = "dev-token"
    debug: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()

