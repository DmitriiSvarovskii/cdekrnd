from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards import unresolved_tickets_kb
from src.lexicons import manager_text

router = Router(name=__name__)


@router.callback_query(F.data == 'view_unresolved_tickets')
async def process_view_unresolved_tickets(
    callback: CallbackQuery,
):
    keyboard_markup = await unresolved_tickets_kb.create_kd_unresolved_tickets(
        user_id=callback.message.chat.id,
    )
    await callback.message.edit_text(
        text=manager_text.common_manager_text['unprocessed_inquiries'],
        reply_markup=keyboard_markup
    )
