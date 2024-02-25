from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from src.lexicons import manager_text


router = Router(name=__name__)


@router.callback_query(F.data == 'press_pass')
async def process_pass(
    callback: CallbackQuery,
):
    await callback.answer(
        text=manager_text.common_manager_text['invalid_request_message']
    )


async def send_echo(message: Message):
    try:
        pass
    except TypeError:
        pass
