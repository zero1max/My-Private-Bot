from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_msg = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Savol yuborish✍🏻")]
        ]
)