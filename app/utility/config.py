from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'mysql+pymysql://root:rootpassword@billing_database:3306/billing_db'
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

