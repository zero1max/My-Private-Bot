import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp,bot
from database.db_handlers import setup_users, setup_events, setup_old_events, move_old_events
import handlers


async def main():
    await setup_users()
    await setup_events()
    await setup_old_events()
    # Scheduler sozlash
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(move_old_events, "cron", hour=0, minute=1)  # har kuni soat 00:01 da
    scheduler.start()
    #
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())