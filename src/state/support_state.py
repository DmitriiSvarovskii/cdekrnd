from aiogram.filters.state import State, StatesGroup


class FSMSupport(StatesGroup):
    waiting_for_manager_response = State()
    manager_response = State()
    client_question = State()
    finished_support = State()
