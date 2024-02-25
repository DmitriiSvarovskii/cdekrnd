from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_kb_close_wayllib() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отменить регистрацию накладной')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
