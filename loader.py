import os 
from dotenv import load_dotenv
#
from aiogram import Dispatcher , Router, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


load_dotenv()

TOKEN = os.getenv("TOKEN")

dp = Dispatcher()
router = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # type: ignore
dp.include_router(router=router)