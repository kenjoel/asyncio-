from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_DELTA: int
    REFRESH_EXPIRATION_DELTA: int
    ACCESS_TOKEN_EXPIRATION_DELTA: int

    class Config:
        env_file = ".env"


settings = Settings()
