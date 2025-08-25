import aiosqlite
from datetime import date


DB = 'users.db'

async def setup_users():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                surname TEXT NOT NULL
            )
        """)
        await db.commit()

async def add_user(user_id, full_name, surname):
    async with aiosqlite.connect(DB) as db:
        # Avval user mavjudligini tekshiramiz
        async with db.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,)) as cursor:
            count = (await cursor.fetchone())[0] # type: ignore

        if count == 0:  # Agar mavjud bo‘lmasa qo‘shamiz
            await db.execute(
                "INSERT INTO users (user_id, full_name, surname) VALUES (?, ?, ?)",
                (user_id, full_name, surname)
            )
            await db.commit()

async def select_users():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows   # [(id, user_id, full_name, surname), ...]

async def select_user(id):
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM users WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            return row    # (id, user_id, full_name, surname) yoki None
        
# ============================================================================================

# Jadval yaratish
async def setup_events():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                event_location TEXT NOT NULL,
                event_image TEXT,
                event_register TEXT NOT NULL
            )
        """)
        await db.commit()


# Yangi tadbir qo‘shish
async def add_event(event_name, event_date, event_time, event_location, event_register, event_image=None):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO events (event_name, event_date, event_time, event_location, event_image, event_register)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event_name, event_date, event_time, event_location, event_image, event_register))
        await db.commit()


# Barcha tadbirlarni olish
async def select_events():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM events") as cursor:
            rows = await cursor.fetchall()
            return rows   # [(id, name, date, time, location, image, register), ...]


# Bitta tadbirni olish
async def select_event(id):
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM events WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            return row    # (id, name, date, time, location, image, register) yoki None


# Tadbirni o‘chirish
async def delete_event(id):
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM events WHERE id = ?", (id,))
        await db.commit()

# =======================================================================================

async def setup_old_events():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS old_events(
                id INTEGER PRIMARY KEY,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                event_location TEXT NOT NULL,
                event_image TEXT,
                event_register TEXT NOT NULL
            )
        """)
        await db.commit()


# Eski tadbirlarni ko‘chirish
async def move_old_events():
    today = date.today()

    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM events WHERE event_date < ?", (today.isoformat(),)) as cursor:
            old_rows = await cursor.fetchall()

        if not old_rows:
            return

        for row in old_rows:
            await db.execute("""
                INSERT INTO old_events (id, event_name, event_date, event_time, event_location, event_image, event_register)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)

        await db.execute("DELETE FROM events WHERE event_date < ?", (today.isoformat(),))
        await db.commit()