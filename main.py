import asyncio
import logging
import sys

from loader import dp,bot, db
import handlers.start

async def main():
    await dp.start_polling(bot)
    db.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())