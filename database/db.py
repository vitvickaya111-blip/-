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
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                stage TEXT DEFAULT 'new'
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
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                hours_per_day REAL,
                cost_per_hour REAL,
                monthly_loss REAL,
                yearly_loss REAL,
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
                sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Добавить поле reactivation_sent если его ещё нет
        try:
            await db.execute('ALTER TABLE users ADD COLUMN reactivation_sent INTEGER DEFAULT 0')
        except Exception:
            pass  # колонка уже существует

        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    """Добавить/обновить пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO users (user_id, username, first_name, total_messages)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_interaction = CURRENT_TIMESTAMP,
                total_messages = total_messages + 1
        ''', (user_id, username, first_name))
        await db.commit()


async def get_user(user_id: int):
    """Получить пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            'SELECT user_id, username, first_name, total_messages, stage FROM users WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    'user_id': row[0],
                    'username': row[1],
                    'first_name': row[2],
                    'total_messages': row[3] or 0,
                    'stage': row[4] or 'new'
                }
            return None


async def update_user_stage(user_id: int, stage: str):
    """Обновить этап пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET stage = ? WHERE user_id = ?',
            (stage, user_id)
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


async def save_calculation(user_id: int, hours: float, cost: float,
                          monthly_loss: float, yearly_loss: float):
    """Сохранить расчёт калькулятора"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO calculations
            (user_id, hours_per_day, cost_per_hour, monthly_loss, yearly_loss)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, hours, cost, monthly_loss, yearly_loss))
        await db.commit()


async def get_all_users():
    """Получить всех пользователей для рассылки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT user_id FROM users') as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def get_users_without_funnel():
    """Получить пользователей, у которых нет запланированных сообщений воронки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('''
            SELECT u.user_id FROM users u
            LEFT JOIN funnel_messages fm ON u.user_id = fm.user_id
            WHERE fm.id IS NULL
        ''') as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def schedule_funnel_message(user_id: int, step: int, scheduled_at: str):
    """Запланировать сообщение воронки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO funnel_messages (user_id, step, scheduled_at)
            VALUES (?, ?, ?)
        ''', (user_id, step, scheduled_at))
        await db.commit()


async def has_funnel_messages(user_id: int) -> bool:
    """Проверить есть ли уже запланированные сообщения воронки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            'SELECT COUNT(*) FROM funnel_messages WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            count = (await cursor.fetchone())[0]
            return count > 0


async def get_pending_funnel_messages():
    """Получить сообщения воронки, которые пора отправить"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT id, user_id, step FROM funnel_messages
            WHERE sent = 0 AND scheduled_at <= datetime('now')
        ''') as cursor:
            rows = await cursor.fetchall()
            return [{'id': row['id'], 'user_id': row['user_id'], 'step': row['step']} for row in rows]


async def mark_funnel_message_sent(message_id: int):
    """Пометить сообщение воронки как отправленное"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE funnel_messages SET sent = 1 WHERE id = ?',
            (message_id,)
        )
        await db.commit()


async def get_inactive_users(days: int = 7):
    """Получить пользователей, не заходивших N дней"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('''
            SELECT user_id FROM users
            WHERE last_interaction < datetime('now', ? || ' days')
            AND (reactivation_sent IS NULL OR reactivation_sent = 0)
        ''', (f'-{days}',)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def mark_reactivation_sent(user_id: int):
    """Пометить что реактивация отправлена"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET reactivation_sent = 1 WHERE user_id = ?',
            (user_id,)
        )
        await db.commit()


async def reset_reactivation(user_id: int):
    """Сбросить флаг реактивации (при новом визите)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            'UPDATE users SET reactivation_sent = 0 WHERE user_id = ?',
            (user_id,)
        )
        await db.commit()


async def get_stats():
    """Получить статистику бота"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Всего пользователей
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            total_users = (await cursor.fetchone())[0]

        # Сегодня новых
        async with db.execute(
            "SELECT COUNT(*) FROM users WHERE DATE(created_at) = DATE('now')"
        ) as cursor:
            today_users = (await cursor.fetchone())[0]

        # Заявок на консультацию
        async with db.execute('SELECT COUNT(*) FROM consultations') as cursor:
            total_consultations = (await cursor.fetchone())[0]

        # Брифов
        async with db.execute('SELECT COUNT(*) FROM briefs') as cursor:
            total_briefs = (await cursor.fetchone())[0]

        # Последние 5 пользователей
        async with db.execute(
            'SELECT username, first_name, created_at FROM users ORDER BY created_at DESC LIMIT 5'
        ) as cursor:
            recent_users = await cursor.fetchall()

        return {
            'total_users': total_users,
            'today_users': today_users,
            'total_consultations': total_consultations,
            'total_briefs': total_briefs,
            'recent_users': recent_users
        }
