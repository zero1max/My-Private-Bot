from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
#
from loader import router, bot
from keyboards.keybords import *
from .states import *


#--------------------------------------------------Savol yuborish--------------------------------------------------------
@router.message(F.text == "Savol yuborish✍🏻")
async def get_msg(msg: Message, state: FSMContext): # type: ignore
    await state.set_state(MSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!") # type: ignore

@router.message(MSG.messaga)
async def question(msg: Message, state: FSMContext): # type: ignore
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id # type: ignore
    user_name = msg.from_user.full_name # type: ignore
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]])
    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>💬Sizda yangi xabar mavjud</b>\n\n<b>Savol yuboruvchi:</b> {user_name}\n<b>Savol:</b> {text}", reply_markup=answer_key) # type: ignore
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext): # type: ignore
    user_id = call.data.split(':') # type: ignore
    await state.update_data(user_id = user_id[1])
    await state.set_state(Answer.asnwer)
    await bot.send_message(ADMIN_ID, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Muhammadjon") # type: ignore

@router.message(Answer.asnwer)
async def answer(msg:Message, state:FSMContext): # type: ignore
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>")

#--------------------------------------------------Anonim Savol yuborish--------------------------------------------------------
@router.message(F.text == "Anonim savol yuborish🤫✍️")
async def get_msg(msg: Message, state: FSMContext):
    await state.set_state(anonimMSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!") # type: ignore

@router.message(anonimMSG.messaga)
async def question(msg: Message, state: FSMContext):
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id # type: ignore
    user_name = msg.from_user.full_name # type: ignore
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]]) # type: ignore
    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>💬Sizda yangi xabar mavjud</b>\n\n<b>Savol</b>: {text}", reply_markup=answer_key) # type: ignore
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':') # type: ignore
    await state.update_data(user_id = user_id[1])
    await state.set_state(anonimAnswer.asnwer)
    await bot.send_message(ADMIN_ID, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Muhammadjon") # type: ignore

@router.message(anonimAnswer.asnwer)
async def answer(msg:Message, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>")
