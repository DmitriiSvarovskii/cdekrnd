from aiogram.filters.state import State, StatesGroup


class FSMManagerRegistration(StatesGroup):
    counter = State()
