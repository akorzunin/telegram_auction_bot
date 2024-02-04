import os
from dotenv import load_dotenv

load_dotenv()

# telegram bot token
TOKEN = os.getenv("TOKEN")
DEBUG = bool(eval(os.getenv("DEBUG", "False")))

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID")

PORT = int(os.getenv("PORT", 8001))
# default to servece name in docker-compose file
API_ENDPOINT = os.getenv("API_ENDPOINT", f"http://telegrambotapi:{PORT}")
