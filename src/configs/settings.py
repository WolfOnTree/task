from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class ApiConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    project_name: str = "DefaultApi"
    project_port: int = 8000
    project_host: str = "127.0.0.1"

    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432

    db_dsl: URL | None = None

    @model_validator(mode="after")
    def set_db_dsl(self):
        self.db_dsl = URL.create(
            "postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )
        
        return self

settings = ApiConfig()

print(settings.model_dump())