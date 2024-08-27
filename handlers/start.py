from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F
from aiogram.filters import CommandStart, Command
import hashlib
from loader import router, bot, db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.keybords import *

ADMIN_ID = 'ADMIN_ID'

#-------------------------FOR HASH STATES -----------------------
class HashState(StatesGroup):
    hashmessage = State()

#-------------------------FOR CHAT STATES------------------------
class MSG(StatesGroup):
    messaga = State()

class Answer(StatesGroup):
    asnwer = State()

#---------------------------------------------------START MAIN--------------------------------------------------------------
@router.message(CommandStart()) 
async def start(msg: Message):
    db.create_table()
    if msg.from_user.id == ADMIN_ID:
        await msg.answer("<b>Assalomu aleykum Muhammadjon!</b>")
    else:
        await msg.answer_sticker('CAACAgIAAxkBAAMHZdstv1FOKr6gphvJjivr8M8KsskAAlQAA0G1Vgxqt_jHCI0B-jQE')
        await msg.answer(f"<b>Assalomu aleykum </b>{msg.from_user.full_name}<b>!😊\nMening shaxsiy botimga xush kelibsiz!👨🏻‍💻</b>")
        await msg.answer("<b>Taklif va savollaringiz bo'lsa yozishingiz mumkin!✍🏻</b>", reply_markup=send_msg)


#--------------------------------------------------Savol yuborish--------------------------------------------------------
@router.message(F.text == "Savol yuborish✍🏻")
async def get_msg(msg: Message, state: FSMContext):
    await state.set_state(MSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!")

@router.message(MSG.messaga)
async def question(msg: Message, state: FSMContext):
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]])
    await bot.send_message(chat_id=ADMIN_ID, text=f"Savol yuboruvchi: {user_name}\nSavol: {text}", reply_markup=answer_key)
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':')
    await state.update_data(user_id = user_id[1])
    await state.set_state(Answer.asnwer)
    await bot.send_message(ADMIN_ID, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Muhammadjon")

@router.message(Answer.asnwer)
async def answer(msg:Message, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>")


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
     await msg.answer(f"Sizning ID: <b>{msg.from_user.id}</b>")

#------------------------------------------------Sticker--------------------------------------------------------
@router.message(F.sticker)
async def echo_sticker(msg: Message):
    await msg.answer(f"Siz yuborgan stiker identifikatori:\n{msg.sticker.file_id}")

#-------------------------------------------------Photo--------------------------------------------------------
@router.message(F.photo)
async def echo_photo(msg: Message):
    photo_id = msg.photo[-1].file_id
    await msg.answer(f"Siz yuborgan photo identifikatori: \n{photo_id}")

#-------------------------------------------------Document--------------------------------------------------------
@router.message(F.document)
async def echo_document(msg: Message):
    document_id = msg.document.file_id
    await msg.answer(f"Siz yuborgan document identifikatori: \n{document_id}")

#-------------------------------------------------Video--------------------------------------------------------
@router.message(F.video)
async def echo_video(msg: Message):
    video_id = msg.video.file_id
    await msg.answer(f"Siz yuborgan video identifikatori: \n{video_id}")
    