import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 255724496))
DATABASE_PATH = "database/bot.db"
INSTAGRAM_URL = "https://instagram.com/podruga_iz_brazilii"
