import asyncio
import logging
import sys

from loader import dp,bot
from database.db_handlers import setup_users, setup_events
import handlers


async def main():
    await setup_users()
    await setup_events()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())