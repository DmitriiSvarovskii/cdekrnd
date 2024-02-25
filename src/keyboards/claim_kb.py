import math
from typing import List, Optional, Union
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
)

from src.schemas import claim_schemas
from src.lexicons import manager_text, customer_text
from src.callbacks import (
    ClaimCallbackFactory,
    ClaimPageCallbackFactory,
    ClaimDocumentCallbackFactory,
    ClaimtViewedPageCallbackFactory,
    ClaimtViewedCallbackFactory
)


async def create_kb_claim_list(
    user_id: int,
    data: List[claim_schemas.ReadClaim],
    callback_factory: Union[
        ClaimCallbackFactory | ClaimtViewedCallbackFactory
    ],
    callback_factory_page: Union[
        ClaimPageCallbackFactory | ClaimtViewedPageCallbackFactory
    ],
    current_page: Optional[int] = 0,
):
    keyboard = InlineKeyboardBuilder()
    if data:
        total_pages = max(math.ceil(len(data) / 5), 1)

        for item in data[current_page * 5: (current_page + 1) * 5]:
            keyboard.row(
                InlineKeyboardButton(
                    text=f'Претензия №{item.id} от клиента №{user_id}',
                    callback_data=ClaimCallbackFactory(
                        id=item.id, user_id=user_id
                    ).pack()
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
        manager_text.claims_manager_text['viewed_claims']
        if callback_factory == ClaimCallbackFactory
        else manager_text.claims_manager_text['new_claims']
    )
    keyboard.row(
        InlineKeyboardButton(
            text=archive_text,
            callback_data=(
                'press_viewed_claims'
                if callback_factory == ClaimCallbackFactory
                else 'press_claims_list'
            )
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.common_manager_text['main_menu'],
            callback_data='press_main_menu_manager'
        ), width=1
    )

    return keyboard.as_markup()


def create_kb_close_claim():
    button = KeyboardButton(
        text=customer_text.claims_cust_btn['cancel_claim_filling'])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard


def create_kb_close_or_done_claim():
    button = KeyboardButton(text=customer_text.claims_cust_btn['submit_claim'])
    button_2 = KeyboardButton(
        text=customer_text.claims_cust_btn['cancel_claim_filling'])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_2, button]],
        resize_keyboard=True
    )
    return keyboard


async def create_kb_claim_one(
    data: Optional[claim_schemas.ReadClaim],
):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.claims_manager_text['photos_documents'],
            callback_data=ClaimDocumentCallbackFactory(id=data.id).pack()
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=manager_text.claims_manager_text['viewed_claims'],
            callback_data='press_viewed_claims'
        ),
        InlineKeyboardButton(
            text=manager_text.common_manager_text['main_menu'],
            callback_data='press_main_menu_manager'
        ), width=1
    )

    return keyboard.as_markup()
