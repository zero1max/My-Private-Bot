from aiogram.fsm.state import StatesGroup, State


#-------------------------FOR HASH STATES -----------------------
class HashState(StatesGroup):
    hashmessage = State()

#-------------------------FOR CHAT STATES------------------------
class MSG(StatesGroup):
    messaga = State()

class Answer(StatesGroup):
    asnwer = State()

class anonimMSG(StatesGroup):
    messaga = State()

class anonimAnswer(StatesGroup):
    asnwer = State()

# ------------------------ CREATE EVENT -----------------------------
class EventStates(StatesGroup):
    name = State()
    date = State()
    time = State()
    location = State()
    register = State()
    image = State()

class DeleteIDStates(StatesGroup):
    id = State()