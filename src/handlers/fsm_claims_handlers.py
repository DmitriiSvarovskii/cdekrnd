# from typing import Union

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext


from src.schemas import claim_schemas
from src.state import claims_state as cl_state
# from src.db import customer_db, claim_db, manager_db
from src.keyboards import start_kb, claim_kb
from src.lexicons import manager_text, customer_text
from src.utils import claim_utils

router = Router(name=__name__)


@router.callback_query(F.data == 'press_register_complaint')
async def process_waybill_number(
    calback: CallbackQuery,
    state: FSMContext
):
    await calback.message.answer(
        text=customer_text.claims_cust_text['waybill_number'],
        reply_markup=claim_kb.create_kb_close_claim()
    )
    await state.set_state(cl_state.FSMClaimsRegistration.waybill_number)


@router.message(F.text == "Отменить заполнение претензии")
async def process_cancel_claim(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    await message.answer(
        text=customer_text.claims_cust_text['claim_interruption'],
        reply_markup=ReplyKeyboardRemove()
    )

    manager_id = await claim_utils.process_claim(
        message=message,
        state=state,
        schemas=claim_schemas.ClaimCancelled
    )

    await bot.send_message(
        chat_id=manager_id,
        text=manager_text.claims_manager_text['claim_interrupted'],
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.send_message(
        chat_id=manager_id,
        text=manager_text.common_manager_text['main_menu'],
        reply_markup=await start_kb.create_kb_support_man_main(
            manager_id)
    )


@router.message(cl_state.FSMClaimsRegistration.waybill_number)
async def process_email_for_response(
    message: Message,
    state: FSMContext,
):
    await state.update_data(waybill_number=message.text)
    await message.answer(
        text=customer_text.claims_cust_text['email_for_response'],
        reply_markup=claim_kb.create_kb_close_claim()
    )
    await state.set_state(cl_state.FSMClaimsRegistration.email_for_response)


@router.message(cl_state.FSMClaimsRegistration.email_for_response)
async def process_situation_description(
    message: Message,
    state: FSMContext,
):
    await state.update_data(email_for_response=message.text)
    await message.answer(
        text=customer_text.claims_cust_text['situation_description'],
        reply_markup=claim_kb.create_kb_close_claim()
    )
    await state.set_state(cl_state.FSMClaimsRegistration.situation_description)


@router.message(cl_state.FSMClaimsRegistration.situation_description)
async def process_required_amount(
    message: Message,
    state: FSMContext,
):
    await state.update_data(situation_description=message.text)
    await message.answer(
        text=customer_text.claims_cust_text['required_amount'],
        reply_markup=claim_kb.create_kb_close_claim()
    )
    await state.set_state(cl_state.FSMClaimsRegistration.required_amount)


@router.message(cl_state.FSMClaimsRegistration.required_amount)
async def process_photos_or_scans(
    message: Message,
    state: FSMContext,
):
    await state.update_data(required_amount=message.text)
    await message.answer(
        text=customer_text.claims_cust_text['photos_or_scans'],
        reply_markup=claim_kb.create_kb_close_or_done_claim()
    )
    await state.set_state(cl_state.FSMClaimsRegistration.photos_or_scans)


@router.message(
    cl_state.FSMClaimsRegistration.photos_or_scans,
    F.photo | F.document | F.media_group
)
async def process_photos_or_scans_test(
    message: Message,
    state: FSMContext,
):
    current_state = await state.get_data()

    if message.photo:
        await state.update_data(
            photo=current_state.get(
                'photo', []) + [message.photo[0].file_id]
        )
    elif message.document:
        await state.update_data(
            document=current_state.get(
                'document', []) + [message.document.file_id]
        )

    await state.set_state(cl_state.FSMClaimsRegistration.photos_or_scans)


@router.message(F.text == 'Отправить претензию')
async def process_claim_registration(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    await message.answer(
        text=customer_text.claims_cust_text['claim_registered'],
        reply_markup=ReplyKeyboardRemove()
    )

    manager_id = await claim_utils.process_claim(
        message=message,
        state=state,
        schemas=claim_schemas.ClaimBase
    )

    await bot.send_message(
        chat_id=manager_id,
        text=manager_text.claims_manager_text['new_claim_registered'],
        reply_markup=await start_kb.create_kb_support_man_main(
            manager_id
        )
    )

    await state.clear()


# async def process_claim(
#     message: Message,
#     state: FSMContext,
#     schemas: Union[claim_schemas.ClaimBase | claim_schemas.ClaimCancelled]
# ):
#     customer_data = await customer_db.get_customer(user_id=message.chat.id)
#     manager_data = await manager_db.get_manager_by_id(
#         id=customer_data.manager_id
#     )

#     await state.update_data(customer_id=customer_data.id)
#     data = await state.get_data()
#     await state.clear()

#     filtered_data = {k: v for k,
#                      v in data.items() if k not in ("photo", "document")}

#     claims_data = schemas(**filtered_data)

#     claim_id = await claim_db.create_claim(data=claims_data)

#     claims_document_data = [
#         claim_schemas.ClaimDocumentBase(
#             claim_id=claim_id,
#             document_url=url,
#             type_document='photo' if url in data.get(
#                 'photo', []) else 'document'
#         ) for url in data.get('photo', []) + data.get('document', [])
#     ]

#     if claims_document_data:
#         await claim_db.create_claim_document(data=claims_document_data)

#     await message.answer(
#         text=customer_text.common_cust_text['menu_item_selection'],
#         reply_markup=await start_kb.create_kb_client()
#     )

#     return manager_data.user_id
