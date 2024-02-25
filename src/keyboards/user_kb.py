from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_kb_register_manager() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='отменить регистрацию')
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard
