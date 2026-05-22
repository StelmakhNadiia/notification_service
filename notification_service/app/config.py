import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Notification-Service"
    

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/notification_db")
    
   
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    
    
    SMTP_HOST: str = "smtp.mockmail.com"
    SMTP_PORT: int = 587
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()