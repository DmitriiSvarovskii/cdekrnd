from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards import support_kb
from src.utils import support_utils
from src.lexicons import manager_text
from src.callbacks import (
    SupportPageCallbackFactory,
    SupportCallbackFactory,
    SupportViewedCallbackFactory,
    SupportViewedPageCallbackFactory,
)

router = Router(name=__name__)


@router.callback_query(F.data == 'press_support_list')
async def process_support_list(callback: CallbackQuery):
    data, customer_user_id = await support_utils.get_support_list(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await support_kb.create_kb_support_list(
        user_id=customer_user_id,
        data=data,
        callback_factory=SupportCallbackFactory,
        callback_factory_page=SupportPageCallbackFactory,
    )
    await callback.message.edit_reply_markup(
        text=manager_text.support_manager_text['support_requests'],
        reply_markup=keyboard_markup
    )


@router.callback_query(F.data == 'press_viewed_supports')
async def process_viewed_support_tickets(callback: CallbackQuery):
    data, customer_user_id = await support_utils.get_viewed_support_tickets(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await support_kb.create_kb_support_list(
        user_id=customer_user_id,
        data=data,
        callback_factory=SupportViewedCallbackFactory,
        callback_factory_page=SupportViewedPageCallbackFactory,
    )
    await callback.message.edit_reply_markup(
        text=manager_text.support_manager_text['viewed_support_requests'],
        reply_markup=keyboard_markup
    )


@router.callback_query(SupportViewedPageCallbackFactory.filter())
@router.callback_query(SupportPageCallbackFactory.filter())
async def process_support_list_next_page(
    callback: CallbackQuery,
    callback_data: SupportPageCallbackFactory
):
    data, customer_user_id = await support_utils.get_support_list(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await support_kb.create_kb_support_list(
        user_id=customer_user_id,
        data=data,
        current_page=callback_data.page,
        callback_factory=SupportCallbackFactory,
        callback_factory_page=SupportPageCallbackFactory,
    )
    await callback.message.edit_reply_markup(
        text=manager_text.support_manager_text['support_requests'],
        reply_markup=keyboard_markup
    )


async def process_viewed_support_tickets_next_page(
    callback: CallbackQuery,
    callback_data: SupportPageCallbackFactory
):
    data, customer_user_id = await support_utils.get_viewed_support_tickets(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await support_kb.create_kb_support_list(
        user_id=customer_user_id,
        data=data,
        current_page=callback_data.page,
        callback_factory=SupportViewedCallbackFactory,
        callback_factory_page=SupportViewedPageCallbackFactory,
    )
    await callback.message.edit_reply_markup(
        text=manager_text.support_manager_text['support_requests'],
        reply_markup=keyboard_markup
    )
