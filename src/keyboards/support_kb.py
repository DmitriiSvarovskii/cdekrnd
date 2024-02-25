import math
from typing import List, Optional, Union
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.callbacks import (
    SupportCallbackFactory,
    SupportPageCallbackFactory,
    SupportViewedPageCallbackFactory,
    SupportViewedCallbackFactory
)
from src.schemas import support_schemas
from src.lexicons import manager_text, customer_text


async def create_kb_support_list(
    user_id: int,
    data: List[support_schemas.ReadSupport],
    callback_factory: Union[
        SupportCallbackFactory | SupportViewedCallbackFactory
    ],
    callback_factory_page: Union[
        SupportPageCallbackFactory | SupportViewedPageCallbackFactory
    ],
    current_page: Optional[int] = 0,
):
    keyboard = InlineKeyboardBuilder()

    if data:
        total_pages = max(math.ceil(len(data) / 5), 1)

        for item in data[current_page * 5: (current_page + 1) * 5]:
            keyboard.row(
                InlineKeyboardButton(
                    text=manager_text.support_list_btn_message(
                        user_id=user_id, support_id=item.id
                    ),
                    callback_data=callback_factory(
                        id=item.id, user_id=user_id).pack()
                ), width=1
            )

        pagination_row = [
            InlineKeyboardButton(
                text=manager_text.claims_manager_text['backward']
                if current_page > 0 else " ",
                callback_data="press_pass" if current_page == 0
                else callback_factory_page(
                    page=max(current_page - 1, 0)).pack()
            ),
            InlineKeyboardButton(
                text=f"{current_page + 1}/{total_pages}",
                callback_data="press_pass"
            ),
            InlineKeyboardButton(
                text=manager_text.claims_manager_text['forward']
                if current_page + 1 < total_pages else " ",
                callback_data="press_pass" if current_page + 1 == total_pages
                else callback_factory_page(
                    page=min(current_page + 1, total_pages - 1)).pack()
            )
        ]
        keyboard.row(*pagination_row)

    archive_text = (
        manager_text.support_manager_text['archive']
        if callback_factory == SupportCallbackFactory
        else manager_text.support_manager_text['new_supports']
    )
    keyboard.row(
        InlineKeyboardButton(
            text=archive_text,
            callback_data='press_viewed_supports'
            if callback_factory == SupportCallbackFactory
            else 'press_support_list'
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.common_manager_text['main_menu'],
            callback_data='press_main_menu_manager'
        ), width=1
    )

    return keyboard.as_markup()


def create_kb_close_support() -> ReplyKeyboardMarkup:
    button = KeyboardButton(
        text=customer_text.support_cust_text['claim_closed_btn']
    )
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


def create_kb_close_support_manager() -> ReplyKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.support_manager_text['claim_closed_btn'],
            callback_data='press_close_support'
        ), width=1
    )
    return keyboard.as_markup()
