
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Django security
SECRET_KEY = os.getenv("SECRET_KEY", "")
DEBUG = os.getenv("DEBUG", "False").strip().lower() in ("true", "1", "yes")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not configured. Please create your .env file.")

# Allowed hosts
allowed_hosts_str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [
    host.strip()
    for host in allowed_hosts_str.split(",")
    if host.strip()
]

# PostgreSQL configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", ""),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

if not all([
    DATABASES["default"]["NAME"],
    DATABASES["default"]["USER"],
    DATABASES["default"]["PASSWORD"],
]):
    raise ValueError("PostgreSQL database configuration is incomplete.")
