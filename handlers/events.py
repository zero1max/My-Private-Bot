from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
#
from .states import *
from loader import bot, router, ADMIN_ID
from keyboards.keybords import *
from database.db_handlers import add_event, select_events, select_event, delete_event


# Tadbirlar ro‘yxati chiqarish
@router.message(F.text == "Tadbirlar 📅")
async def events(msg: Message):
    events = await select_events()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ev[1], callback_data=f"event_{ev[0]}")] for ev in events
        ]
    )

    # faqat admin uchun "➕ Tadbir qo‘shish"
    if msg.from_user.id == ADMIN_ID: # type: ignore
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="➕ Tadbir qo‘shish", callback_data="add_event"),InlineKeyboardButton(text="🆔 Tadbir IDs", callback_data="id_events")] 
        )

    if not events:
        await msg.answer("📭 Hozircha tadbirlar yo‘q.", reply_markup=keyboard)
    else:
        await msg.answer("📅 Tadbirlar ro‘yxati:", reply_markup=keyboard)


# Bitta tadbir tafsilotlari
@router.callback_query(F.data.startswith("event_"))
async def event_detail(callback: CallbackQuery):
    event_id = int(callback.data.split("_")[1])  # type: ignore
    event = await select_event(event_id)

    if not event:
        await callback.answer("Tadbir topilmadi ❌", show_alert=True)
        return

    text = (
        f"📌 <b>{event[1]}</b>\n\n"
        f"📅 Sana: {event[2]}\n"
        f"⏰ Vaqti: {event[3]}\n"
        f"📍 Manzil: {event[4]}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_events")]
        ]
    )

    # Agar rasm bo‘lsa
    if event[5]:
        try:
            await callback.message.delete()  # eski xabarni o‘chiramiz # type: ignore
            await bot.send_photo(
                chat_id=callback.message.chat.id, # type: ignore
                photo=event[5],  # bu file_id
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Rasm yuborishda xatolik: {e}")
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML") # type: ignore
    else:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML") # type: ignore


# Ortga qaytish
@router.callback_query(F.data == "back_to_events")
async def back_to_events(callback: CallbackQuery):
    events = await select_events()

    if not events:
        await callback.message.edit_text("📭 Hozircha tadbirlar yo‘q.") # type: ignore
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ev[1], callback_data=f"event_{ev[0]}")] for ev in events
        ]
    )

    # faqat admin uchun "➕ Tadbir qo‘shish"
    if callback.from_user.id == ADMIN_ID: # type: ignore
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="➕ Tadbir qo‘shish", callback_data="add_event"),InlineKeyboardButton(text="🆔 Tadbir IDs", callback_data="id_events")] 
        )

    await callback.message.delete() # type: ignore
    await callback.message.answer("📅 Tadbirlar ro‘yxati:", reply_markup=keyboard) # type: ignore


# ➕ Tadbir qo‘shishni boshlash (faqat admin)
@router.callback_query(F.data == "add_event")
async def start_add_event(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Bu faqat admin uchun!", show_alert=True)
        return
    await state.set_state(EventStates.name)
    await callback.message.edit_text("📝 Tadbir nomini kiriting:") # type: ignore


# Tadbir nomi
@router.message(EventStates.name)
async def event_name(msg: Message, state: FSMContext):
    await state.update_data(event_name=msg.text)
    await state.set_state(EventStates.date)
    await msg.answer("📅 Tadbir sanasini kiriting (masalan: 2025-09-01):")


# Sana
@router.message(EventStates.date)
async def event_date(msg: Message, state: FSMContext):
    await state.update_data(event_date=msg.text)
    await state.set_state(EventStates.time)
    await msg.answer("⏰ Tadbir vaqtini kiriting (masalan: 10:00 - 18:00):")


# Vaqt
@router.message(EventStates.time)
async def event_time(msg: Message, state: FSMContext):
    await state.update_data(event_time=msg.text)
    await state.set_state(EventStates.location)
    await msg.answer("📍 Tadbir manzilini kiriting (link yoki location matni):")


# Manzil
@router.message(EventStates.location)
async def event_location(msg: Message, state: FSMContext):
    await state.update_data(event_location=msg.text)
    await state.set_state(EventStates.image)
    await msg.answer("🖼 Tadbir rasmi linkini yuboring (yoki 'yo‘q' deb yozing):")


# Rasm
@router.message(EventStates.image)
async def event_image(msg: Message, state: FSMContext):
    image = None

    # Agar text yuborsa
    if msg.text:
        if msg.text.lower() != "yo'q":
            image = msg.text.strip()
    # Agar rasm yuborsa
    elif msg.photo:
        # eng oxirgi (eng sifatli) rasm file_id olinadi
        image = msg.photo[-1].file_id

    data = await state.get_data()
    await add_event(
        data["event_name"],
        data["event_date"],
        data["event_time"],
        data["event_location"],
        image
    )
    await state.clear()
    await msg.answer("✅ Tadbir muvaffaqiyatli qo‘shildi!")

# -------------------------------------------------- IDs Events ------------------------------------------------


# ID va nomlarini chiqarish (faqat admin uchun)
@router.callback_query(F.data == "id_events")
async def id_events(call: CallbackQuery):
    events = await select_events()

    if not events:
        await call.message.edit_text("📭 Hozircha tadbirlar yo‘q.") # type: ignore
        return

    text = "📌 <b>Tadbirlar ro‘yxati (ID bilan)</b>\n\n"
    for ev in events:
        text += f"🆔 <b>{ev[0]}</b> — {ev[1]}\n"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Tadbir o‘chirish", callback_data="delete_event")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_events")]
        ]
    )

    await call.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML") # type: ignore

# O‘chirish tugmasi bosilganda -> event_id so‘raymiz
@router.callback_query(F.data == "delete_event")
async def ask_event_id(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("❓ O‘chirmoqchi bo‘lgan tadbir ID sini kiriting:") # type: ignore
    await state.set_state(DeleteIDStates.id)


# event_id ni qabul qilib, o‘chirib tashlaymiz
@router.message(DeleteIDStates.id)
async def delete_event_by_id(msg: Message, state: FSMContext):
    try:
        event_id = int(msg.text.strip()) # type: ignore
        await delete_event(event_id)  # DB dan o‘chiradi
        await msg.answer(f"✅ Tadbir {event_id} muvaffaqiyatli o‘chirildi!")
    except Exception as e:
        await msg.answer(f"❌ Xatolik: {e}")

    await state.clear()