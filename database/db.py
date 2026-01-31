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
                is_new INTEGER DEFAULT 1,
                funnel_active INTEGER DEFAULT 0,
                consultation_booked INTEGER DEFAULT 0,
                brief_submitted INTEGER DEFAULT 0,
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

        await db.execute('''
            CREATE TABLE IF NOT EXISTS diagnostics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                business TEXT,
                automation TEXT,
                budget TEXT,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS funnel_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                step INTEGER,
                scheduled_at TIMESTAMP,
                sent_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Миграция: добавить новые колонки если их нет
        try:
            await db.execute('ALTER TABLE users ADD COLUMN is_new INTEGER DEFAULT 1')
        except Exception:
            pass
        try:
            await db.execute('ALTER TABLE users ADD COLUMN funnel_active INTEGER DEFAULT 0')
        except Exception:
            pass
        try:
            await db.execute('ALTER TABLE users ADD COLUMN consultation_booked INTEGER DEFAULT 0')
        except Exception:
            pass
        try:
            await db.execute('ALTER TABLE users ADD COLUMN brief_submitted INTEGER DEFAULT 0')
        except Exception:
            pass

        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    """Добавить или обновить пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_interaction = CURRENT_TIMESTAMP
        ''', (user_id, username, first_name))
        await db.commit()


async def is_user_new(user_id: int) -> bool:
    """Проверить, новый ли пользователь"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            'SELECT is_new FROM users WHERE user_id = ?', (user_id,)
        )
        row = await cursor.fetchone()
        if row is None:
            return True
        return bool(row[0])


async def mark_user_not_new(user_id: int):
    """Пометить пользователя как не нового"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET is_new = 0 WHERE user_id = ?', (user_id,)
        )
        await db.commit()


async def save_diagnostics(user_id: int, business: str, automation: str, budget: str, recommendation: str):
    """Сохранить результаты диагностики"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO diagnostics (user_id, business, automation, budget, recommendation)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, business, automation, budget, recommendation))
        await db.commit()


async def activate_funnel(user_id: int):
    """Активировать воронку для пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET funnel_active = 1 WHERE user_id = ?', (user_id,)
        )
        await db.commit()


async def deactivate_funnel(user_id: int):
    """Деактивировать воронку для пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET funnel_active = 0 WHERE user_id = ?', (user_id,)
        )
        await db.execute(
            "UPDATE funnel_messages SET status = 'cancelled' WHERE user_id = ? AND status = 'pending'",
            (user_id,)
        )
        await db.commit()


async def mark_consultation_booked(user_id: int):
    """Пометить, что пользователь записался на консультацию"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET consultation_booked = 1 WHERE user_id = ?', (user_id,)
        )
        await db.commit()
    await deactivate_funnel(user_id)


async def mark_brief_submitted(user_id: int):
    """Пометить, что пользователь отправил бриф"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET brief_submitted = 1 WHERE user_id = ?', (user_id,)
        )
        await db.commit()
    await deactivate_funnel(user_id)


async def schedule_funnel_message(user_id: int, step: int, scheduled_at: str):
    """Запланировать сообщение воронки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO funnel_messages (user_id, step, scheduled_at)
            VALUES (?, ?, ?)
        ''', (user_id, step, scheduled_at))
        await db.commit()


async def get_pending_funnel_messages():
    """Получить все ожидающие сообщения воронки, время которых наступило"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('''
            SELECT fm.id, fm.user_id, fm.step, fm.scheduled_at
            FROM funnel_messages fm
            JOIN users u ON fm.user_id = u.user_id
            WHERE fm.status = 'pending'
              AND fm.scheduled_at <= datetime('now')
              AND u.funnel_active = 1
        ''')
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def mark_funnel_message_sent(message_id: int):
    """Пометить сообщение воронки как отправленное"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE funnel_messages SET status = 'sent', sent_at = datetime('now') WHERE id = ?",
            (message_id,)
        )
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
