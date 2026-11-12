from pydantic import Field
from pydantic_settings import BaseSettings


class Configuracion(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432

    jwt_secreto: str = Field(min_length=32)
    jwt_minutos: int = 60
    admin_usuario: str
    admin_clave: str
    cors_origenes: str = "http://localhost:3000"
    login_limite: str = "5/5 minutes"  # formato de slowapi: "<n>/<n> <unidad>"

    @property
    def url_bd(self) -> str:
        return (f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")


config = Configuracion()
