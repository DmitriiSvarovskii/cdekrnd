from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards import start_kb
from src.lexicons import manager_text

router = Router(name=__name__)


@router.callback_query(F.data == 'press_main_menu_manager')
async def process_main_menu_manager(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        text=manager_text.common_manager_text['main_menu'],
        reply_markup=await start_kb.create_kb_support_man_main(
            user_id=callback.message.chat.id
        )
    )
