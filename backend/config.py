import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

class Settings:
    app_name = os.getenv("APP_NAME", "CampusSpace")
    app_env = os.getenv("APP_ENV", "development")
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = int(os.getenv("API_PORT", "8000"))
    database_path = (ROOT_DIR / os.getenv("DATABASE_PATH", "data/campusspace.db")).resolve()
    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "dev-only-change-me-before-deployment")
    token_expire_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", "720"))
    verification_ttl_minutes = int(os.getenv("VERIFICATION_TTL_MINUTES", "60"))
    default_canteen_visit_minutes = int(os.getenv("DEFAULT_CANTEEN_VISIT_MINUTES", "20"))

settings = Settings()
