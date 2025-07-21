CONFIG = """from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from supabase import create_client


class Settings(BaseSettings):
    # supabase
    DB_USER: str = "postgres"
    DB_NAME: str = "postgres"
    DB_PORT: str = "5432"
    DEV_LOGS: bool = False
    SUPABASE_DB_PASSWORD: str
    SUPABASE_PROJECT_ID: str

    # supabase storage
    SUPABASE_BUCKET: str = "your-bucket-name"

    # supabase auth
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT: str

    @property
    def supabase_connection_string(self):
        # normal url encoding (runtime usage)
        encoded_password = quote_plus(self.SUPABASE_DB_PASSWORD)
        return (
            f"postgresql://{self.DB_USER}.{self.SUPABASE_PROJECT_ID}:{encoded_password}"
            f"@aws-0-us-east-2.pooler.supabase.com:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def async_supabase_connection_string(self):
        return self.supabase_connection_string.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

    @property
    def supabase_connection_string_alembic(self):
        # alembic-compatible connection string with '%%'
        encoded_password = quote_plus(self.SUPABASE_DB_PASSWORD).replace('%', '%%')
        return (
            f"postgresql://{self.DB_USER}.{self.SUPABASE_PROJECT_ID}:{encoded_password}"
            f"@aws-0-us-east-2.pooler.supabase.com:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
    )


load_dotenv()

settings = Settings()

sb_client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
)
"""
