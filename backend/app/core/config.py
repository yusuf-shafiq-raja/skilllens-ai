from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

APP_NAME = "SkillLens AI"
APP_VERSION = "1.0.0"