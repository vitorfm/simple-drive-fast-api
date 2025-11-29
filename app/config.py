from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = False
    
    database_url: str = "sqlite:///./simpledrive.db"
    
    storage_backend: str = "local"
    
    s3_endpoint_url: str = "https://s3.amazonaws.com"
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""
    s3_bucket_name: str = ""
    s3_region: str = "us-east-1"
    
    local_storage_path: str = "./storage"
    
    ftp_host: str = ""
    ftp_port: int = 21
    ftp_username: str = ""
    ftp_password: str = ""
    ftp_base_dir: str = "/storage"
    
    api_token: str = "dev-token"
    
    class Config:
        env_file = ".env"


settings = Settings()

