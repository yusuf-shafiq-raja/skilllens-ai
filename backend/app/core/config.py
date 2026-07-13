from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

APP_NAME = "SkillLens AI"
APP_VERSION = "1.0.0"

SECRET_KEY = "skilllens_super_secret_key_change_this_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60