import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле!")

try:
    ADMIN_ID = int(os.getenv('ADMIN_ID', 255724496))
except ValueError:
    raise ValueError("ADMIN_ID должен быть числом!")

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "bot.db")
INSTAGRAM_URL = "https://instagram.com/anastasiia_vibecoding_ai"
