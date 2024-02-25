from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.utils import user_utils
from src.keyboards import start_kb

router = Router(name=__name__)


@router.callback_query(F.data == 'press_register_customer')
async def process_register_customer(callback: CallbackQuery):
    await user_utils.create_customer(callback=callback)
    await callback.message.answer(
        text='Client',
        reply_markup=await start_kb.create_kb_client()
    )
