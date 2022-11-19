from pydantic import BaseSettings


class Settings(BaseSettings):
    client_id: str
    secret: str
    app_name: str

    class Config:
        env_file = "../.env"


settings = Settings()
