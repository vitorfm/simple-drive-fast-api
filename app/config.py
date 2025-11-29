from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    storage_backend: str = "local"
    database_url: str = "sqlite:///./simpledrive.db"
    local_storage_path: str = "./storage"
    api_token: str = "dev-token"
    debug: bool = False
    
    s3_endpoint_url: str = ""
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""
    s3_bucket_name: str = ""
    s3_region: str = "us-east-1"
    
    ftp_host: str | None = None
    ftp_port: int = 21
    ftp_username: str = "anonymous"
    ftp_password: str = ""
    ftp_base_dir: str = "/"
    
    class Config:
        env_file = ".env"


settings = Settings()

