from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# ==================================================
# Application
# ==================================================

APP_NAME = "SkillLens AI"
APP_VERSION = "1.0.0"

# ==================================================
# Database
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL")

# ==================================================
# JWT Authentication
# ==================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key-for-development"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        60
    )
)