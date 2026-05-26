import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024
