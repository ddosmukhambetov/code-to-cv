from pathlib import Path

from environs import Env
from pydantic import BaseModel, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(str(BASE_DIR / '.env'))


class AppConfig(BaseModel):
    project_name: str = env.str('PROJECT_NAME')
    project_version: str = env.str('PROJECT_VERSION')
    project_debug: bool = env.bool('PROJECT_DEBUG')
    project_host: str = env.str('PROJECT_HOST')
    project_port: int = env.int('PROJECT_PORT')


class DatabaseConfig(BaseModel):
    url: PostgresDsn = env.str('DATABASE_URL')
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings:
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
