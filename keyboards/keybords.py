from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_msg = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Savol yuborish✍🏻")],
        [KeyboardButton(text="Anonim savol yuborish🤫✍️")],
        [KeyboardButton(text="Tadbirlar 📅")]
    ]
)

admin_key = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Tadbirlar 📅")]
    ]
)