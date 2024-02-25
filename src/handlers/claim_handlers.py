from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.keyboards import claim_kb, start_kb
from src.utils import claim_utils
from src.db import claim_db
from src.lexicons import manager_text
from src.callbacks import (
    ClaimPageCallbackFactory,
    ClaimCallbackFactory,
    ClaimDocumentCallbackFactory,
    ClaimtViewedCallbackFactory,
    ClaimtViewedPageCallbackFactory
)

router = Router(name=__name__)


@router.callback_query(F.data == 'press_claims_list')
async def process_claim_list(callback: CallbackQuery):
    data, customer_user_id = await claim_utils.get_claim_list(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await claim_kb.create_kb_claim_list(
        user_id=customer_user_id,
        data=data,
        callback_factory=ClaimCallbackFactory,
        callback_factory_page=ClaimPageCallbackFactory
    )
    await callback.message.edit_reply_markup(
        text=manager_text.support_manager_text['support_requests'],
        reply_markup=keyboard_markup
    )


@router.callback_query(F.data == 'press_viewed_claims')
async def process_viewed_claim_tickets(callback: CallbackQuery):
    data, customer_user_id = await claim_utils.get_viewed_claim_tickets(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await claim_kb.create_kb_claim_list(
        user_id=customer_user_id,
        data=data,
        callback_factory=ClaimtViewedCallbackFactory,
        callback_factory_page=ClaimtViewedPageCallbackFactory,
    )
    await callback.message.edit_reply_markup(
        text=manager_text.claims_manager_text['viewed_claims'],
        reply_markup=keyboard_markup
    )


@router.callback_query(ClaimPageCallbackFactory.filter())
async def process_claim_list_next_page(
    callback: CallbackQuery,
    callback_data: ClaimPageCallbackFactory
):
    data, customer_user_id = await claim_utils.get_claim_list(
        user_id=callback.message.chat.id
    )
    keyboard_markup = await claim_kb.create_kb_claim_list(
        user_id=customer_user_id,
        data=data,
        current_page=callback_data.page,
        callback_factory=ClaimCallbackFactory,
        callback_factory_page=ClaimPageCallbackFactory
    )
    await callback.message.edit_reply_markup(
        text=manager_text.claims_manager_text['claims_list'],
        reply_markup=keyboard_markup
    )


@router.callback_query(ClaimCallbackFactory.filter())
async def process_one_claim(
    callback: CallbackQuery,
    callback_data: ClaimCallbackFactory
):
    data_one_claim = await claim_db.get_one_claim_db(
        id=callback_data.id
    )
    text = await manager_text.create_claim_text(
        data=data_one_claim,
        customer_user_id=callback_data.user_id)

    await claim_db.change_avail_claim(callback_data.id)

    keyboard_markup = await claim_kb.create_kb_claim_one(
        data=data_one_claim,
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard_markup
    )


@router.callback_query(ClaimDocumentCallbackFactory.filter())
async def process_claim_document(
    callback: CallbackQuery,
    callback_data: ClaimDocumentCallbackFactory
):
    data = await claim_db.get_claim_document_list_db(
        claim_id=callback_data.id
    )
    if data:
        for item in data:
            if item.type_document == 'photo':
                await callback.message.answer_photo(
                    photo=item.document_url
                )
            elif item.type_document == 'document':
                await callback.message.answer_document(
                    document=item.document_url
                )

        await callback.message.answer(
            text=manager_text.common_manager_text['main_menu'],
            reply_markup=await start_kb.create_kb_support_man_main(
                user_id=callback.message.chat.id
            )
        )
    else:
        await callback.answer(
            text=manager_text.claims_manager_text['missing_photos_documents'],
            show_alert=True
        )
