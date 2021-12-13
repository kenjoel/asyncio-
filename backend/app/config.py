from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION_DELTA: int
    REFRESH_EXPIRATION_DELTA: int
    ENGINE_OPTIONS: dict

    class Config:
        env_file = ".env"


settings = Settings()
