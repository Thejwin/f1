from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mode_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_CONNECTION: str

settings = Settings()