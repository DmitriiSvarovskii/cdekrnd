from typing import Union
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.schemas import claim_schemas
from src.db import claim_db, customer_db, manager_db
from src.lexicons import customer_text
from src.keyboards import start_kb


async def get_claim_list(user_id: int):
    manager_data = await manager_db.get_manager(user_id=user_id)
    customer_data = await customer_db.get_customer_by_manag_id(
        manager_id=manager_data.id)
    claim_list = await claim_db.get_claim_list_db(
        customer_id=customer_data.id
    )
    return claim_list, customer_data.user_id


async def get_viewed_claim_tickets(user_id: int):
    manager_data = await manager_db.get_manager(user_id=user_id)
    customer_data = await customer_db.get_customer_by_manag_id(
        manager_id=manager_data.id)
    claim_list = await claim_db.get_viewed_claim_tickets_db(
        customer_id=customer_data.id
    )
    return claim_list, customer_data.user_id


async def process_claim(
    message: Message,
    state: FSMContext,
    schemas: Union[claim_schemas.ClaimBase | claim_schemas.ClaimCancelled]
):
    customer_data = await customer_db.get_customer(user_id=message.chat.id)
    manager_data = await manager_db.get_manager_by_id(
        id=customer_data.manager_id
    )

    await state.update_data(customer_id=customer_data.id)
    data = await state.get_data()
    await state.clear()

    filtered_data = {k: v for k,
                     v in data.items() if k not in ("photo", "document")}

    claims_data = schemas(**filtered_data)

    claim_id = await claim_db.create_claim(data=claims_data)

    claims_document_data = [
        claim_schemas.ClaimDocumentBase(
            claim_id=claim_id,
            document_url=url,
            type_document='photo' if url in data.get(
                'photo', []) else 'document'
        ) for url in data.get('photo', []) + data.get('document', [])
    ]

    if claims_document_data:
        await claim_db.create_claim_document(data=claims_document_data)

    await message.answer(
        text=customer_text.common_cust_text['menu_item_selection'],
        reply_markup=await start_kb.create_kb_client()
    )

    return manager_data.user_id
