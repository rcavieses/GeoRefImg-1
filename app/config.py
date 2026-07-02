import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Ignorar campos extra del .env
    )

    # App
    app_name: str = os.getenv("APP_NAME", "Atlantis Poligons")
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "false").lower() in ("true", "1", "yes")

    # Azure SQL
    azure_sql_server: str = os.getenv("AZURE_SQL_SERVER", "")
    azure_sql_database: str = os.getenv("AZURE_SQL_DATABASE", "")
    azure_sql_user: str = os.getenv("AZURE_SQL_USER", "")
    azure_sql_password: str = os.getenv("AZURE_SQL_PASSWORD", "")
    azure_sql_port: int = int(os.getenv("AZURE_SQL_PORT", "1433"))

    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Sentry
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")

    @property
    def database_url(self) -> str:
        if self.app_env == "development":
            return "sqlite:///./app.db"
        # Formato: mssql+pymssql://user:password@server/database
        # pymssql es compatible con Streamlit Cloud
        return (
            f"mssql+pymssql://{self.azure_sql_user}:{self.azure_sql_password}"
            f"@{self.azure_sql_server}:{self.azure_sql_port}/{self.azure_sql_database}"
        )

settings = Settings()
