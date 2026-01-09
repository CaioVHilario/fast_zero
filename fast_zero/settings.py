from pydantic_settings import BaseSettings, SettingsConfigDict


# classe para pegar o .env onde tem o endereço do db
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
