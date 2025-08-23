import aiosqlite


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

async def setup_events():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                event_location TEXT NOT NULL,
                event_image TEXT
            )
        """)
        await db.commit()


async def add_event(event_name, event_date, event_time, event_location, event_image=None):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO events (event_name, event_date, event_time, event_location, event_image)
            VALUES (?, ?, ?, ?, ?)
        """, (event_name, event_date, event_time, event_location, event_image))
        await db.commit()


async def select_events():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM events") as cursor:
            rows = await cursor.fetchall()
            return rows   # [(id, name, date, time, location, image), ...]


async def select_event(id):
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT * FROM events WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            return row    # (id, name, date, time, location, image) yoki None


async def delete_event(id):
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM events WHERE id = ?", (id,))
        await db.commit()