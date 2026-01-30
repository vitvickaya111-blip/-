import aiosqlite
from config import DATABASE_PATH


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                business TEXT,
                task TEXT,
                contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'новая',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                brief_type TEXT,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'новая',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    """Добавить пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        await db.commit()


async def save_consultation(user_id: int, name: str, business: str, task: str, contact: str):
    """Сохранить заявку на консультацию"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO consultations (user_id, name, business, task, contact)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, business, task, contact))
        await db.commit()


async def save_brief(user_id: int, brief_type: str, data: str):
    """Сохранить бриф"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO briefs (user_id, brief_type, data)
            VALUES (?, ?, ?)
        ''', (user_id, brief_type, data))
        await db.commit()
