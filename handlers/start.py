import hashlib
#
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
#
from .states import *
from loader import router, bot, ADMIN_ID
from keyboards.keybords import *
from database.db_handlers import add_user


#---------------------------------------------------START MAIN--------------------------------------------------------------
@router.message(CommandStart()) 
async def start(msg: Message):
    full_name = msg.from_user.full_name # type: ignore
    surname = msg.from_user.last_name or '' # type: ignore
    user_id = msg.from_user.id # type: ignore

    if user_id == ADMIN_ID:
        await msg.answer_sticker('CAACAgIAAxkBAAMHZdstv1FOKr6gphvJjivr8M8KsskAAlQAA0G1Vgxqt_jHCI0B-jQE')
        await msg.answer("<b>Assalomu aleykum Muhammadjon!</b>", reply_markup=admin_key)
    else:
        await add_user(user_id, full_name, surname)
        await msg.answer_sticker('CAACAgIAAxkBAAMHZdstv1FOKr6gphvJjivr8M8KsskAAlQAA0G1Vgxqt_jHCI0B-jQE')
        await msg.answer(
            f"<b>Assalomu aleykum, {msg.from_user.full_name}!</b> 😊\n" # type: ignore
            f"👨🏻‍💻 <b>Mening shaxsiy botimga xush kelibsiz!</b>\n\n"
            f"<b>Bot haqida qisqacha ma'lumot:</b>\n"
            f"/id - O'zingizning Telegram ID raqamingizni bilish uchun bu buyruqni ishlating.\n"
            f"/hash - Matningizni kriptografik xesh kodga aylantirish. "
            f"Bu funksiya orqali siz ma'lumotlaringizni xavfsiz saqlashingiz mumkin. Xeshlangan ma'lumotlar qayta tiklanmaydi, "
            f"bu esa parollar va shaxsiy ma'lumotlarni himoya qilish uchun juda foydali.\n"
            f"/help - Bot imkoniyatlari va undan foydalanish bo'yicha to'liq ma'lumot olish.\n"
            f"/info - Bot yaratilish tarixi va dasturchi haqida qisqacha ma'lumot.\n\n"
            f"Yana savollaringiz yoki takliflaringiz bo'lsa, bemalol yozishingiz mumkin! "
            f"Botimizdan foydalanayotganingizdan xursandmiz! 😊")


        await check_subscription(msg)
        
async def check_subscription(message: Message):
    channel_ids = ["@zero1max", "@zero1maxdev"]  # Kanal username'lari yoki ID'lari
    channel_urls = {
        "@zero1max": "https://t.me/zero1max",
        "@zero1maxdev": "https://t.me/zero1maxdev"
    }
    user_id = message.from_user.id # type: ignore
    subscribed_channels = set()  

    for channel_id in channel_ids:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status != 'left':
                subscribed_channels.add(channel_id) 
        except Exception as e:
            print(f"Kanal tekshirishda xatolik: {channel_id} - {e}")

    not_subscribed_channels = set(channel_ids) - subscribed_channels

    inline_keyboard = []

    for channel_id in not_subscribed_channels:
        inline_keyboard.append([InlineKeyboardButton(text=f"{channel_id[1:]}", url=channel_urls[channel_id])])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    if not_subscribed_channels:
        await message.answer(
            "Kanallarga obuna bo'lishingizni so'raymiz.\nObuna bo'lgandan so'ng /start buyrug'ini yuboring!\nIltimos, quyidagi kanallarga obuna bo'ling:👇🏻",
            reply_markup=markup
        )
    else:
        await message.answer("<b>Taklif va savollaringiz bo'lsa yozishingiz mumkin!✍🏻</b>", reply_markup=send_msg)


#---------------------------------------------------HASHLIB ----------------------------------------------------------------
@router.message(Command('hash'))
async def hashlash(msg: Message, state: FSMContext):
    await state.set_state(HashState.hashmessage)
    await msg.answer("Hash lamoqchi bo'lgan so'zingizni yuboring!")

@router.message(HashState.hashmessage)
async def hash_msg(msg: Message, state: FSMContext):
    await state.update_data(hashmessage=msg.text)
    data = await state.get_data()
    txt_data = data.get('hashmessage')
    md5_data = hashlib.md5(str(txt_data).encode('utf-8'))
    await msg.answer(f"md5 da: \n<b>{md5_data.hexdigest()}</b>\n")
    
#------------------------------------------------ID--------------------------------------------------------
@router.message(Command('id'))
async def echo_id(msg: Message):
     await msg.answer(f"Sizning ID: <b>{msg.from_user.id}</b>") # type: ignore

#------------------------------------------------HELP------------------------------------------------------
@router.message(Command('help'))
async def help(msg: Message):
    await msg.reply("<b>Botda qandaydur uzulushlar yoki muammolar yuzaga kelsa @zero_1_max ga murojaat qiling!</b>")

#------------------------------------------------INFO-------------------------------------------------------
@router.message(Command('info'))
async def info(msg: Message):
    await msg.answer(
        "<b>Bot haqida ma'lumot:</b>\n\n"
        "Bu bot sizga bir qancha qulay xizmatlarni taqdim etish uchun yaratilgan. "
        "Bot orqali siz o'zingizning ID raqamingizni bilib olishingiz, matnlaringizni xavfsiz tarzda hashlashingiz, "
        "yoki boshqa foydali buyruqlardan foydalanishingiz mumkin.\n\n"
        "<b>Yaratilgan sana:</b> 2024 yil, avgust\n"
        "<b>Dasturchi:</b> @zero_1_max\n\n"
        "Dasturchi bilan bog'lanish yoki qo'shimcha savollar uchun yuqoridagi username orqali murojaat qilishingiz mumkin. "
        "Botimizdan foydalanayotganingiz uchun tashakkur! 😊"
    )

# #------------------------------------------------Sticker--------------------------------------------------------
# @router.message(F.sticker)
# async def echo_sticker(msg: Message):
#     await msg.answer(f"Siz yuborgan stiker identifikatori:\n{msg.sticker.file_id}") # type: ignore

# #-------------------------------------------------Photo--------------------------------------------------------
# @router.message(F.photo)
# async def echo_photo(msg: Message):
#     photo_id = msg.photo[-1].file_id # type: ignore
#     await msg.answer(f"Siz yuborgan photo identifikatori: \n{photo_id}")

# #-------------------------------------------------Document--------------------------------------------------------
# @router.message(F.document)
# async def echo_document(msg: Message):
#     document_id = msg.document.file_id # type: ignore
#     await msg.answer(f"Siz yuborgan document identifikatori: \n{document_id}")

# #-------------------------------------------------Video--------------------------------------------------------
# @router.message(F.video)
# async def echo_video(msg: Message):
#     video_id = msg.video.file_id # type: ignore
#     await msg.answer(f"Siz yuborgan video identifikatori: \n{video_id}")
    