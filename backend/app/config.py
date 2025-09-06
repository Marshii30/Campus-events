import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:password@127.0.0.1:3306/campus_events")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "super-secret-admin-token")
    JSON_SORT_KEYS = False
