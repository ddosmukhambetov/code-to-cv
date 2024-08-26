import uuid
from datetime import datetime
from pathlib import Path

from environs import Env
from pydantic import BaseModel, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env()
env.read_env(str(BASE_DIR / '.env'))


class AppConfig(BaseModel):
    name: str = env.str('APP_NAME')
    version: str = env.str('APP_VERSION')
    debug: bool = env.bool('APP_DEBUG')
    host: str = env.str('APP_HOST')
    port: int = env.int('APP_PORT')


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


class AuthConfig(BaseModel):
    token_secret_key: str = env.str('JWT_SECRET_KEY')
    algorithm: str = env.str('JWT_ALGORITHM')
    access_token_expire_minutes: int = 15


class SqlAdminConfig(BaseModel):
    sqladmin_secret_key: str = env.str('SQLADMIN_SECRET_KEY')


class ApiKeysConfig(BaseModel):
    github_pat: str = env.str('GITHUB_PAT')
    openai_key: str = env.str('OPENAI_API_KEY')


class MediaConfig(BaseModel):
    media_path: str = BASE_DIR / 'media'
    cv_templates_path: str = BASE_DIR / 'templates' / 'cvs'

    @property
    def get_cv_pdf_file_path(self) -> str:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        random_uuid = uuid.uuid4()
        relative_path = Path(f'cvs/{year}/{month}/{day}/cv_{random_uuid}.pdf')
        full_path = self.media_path / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return str(full_path)


class CachingConfig(BaseModel):
    redis_url: str = env.str('REDIS_URL')


class Settings:
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    auth: AuthConfig = AuthConfig()
    admin: SqlAdminConfig = SqlAdminConfig()
    api_keys: ApiKeysConfig = ApiKeysConfig()
    media: MediaConfig = MediaConfig()
    caching: CachingConfig = CachingConfig()


settings = Settings()
