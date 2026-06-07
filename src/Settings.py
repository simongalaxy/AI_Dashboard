import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    
    # define the settings for the application.
    model_name: str
    model_provider: str
    openai_api_base: str
    openai_api_key: str

    # model_provider: str
    # huggingface_token: str
    # huggingface_model: str
    
    # pydantic settings config.
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Singleton instance of the settings.
settings = Settings() # type: ignore
