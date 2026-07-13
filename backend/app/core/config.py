from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = "SkillLens AI"
APP_VERSION = "1.0.0"

DATABASE_URL = os.getenv("DATABASE_URL")