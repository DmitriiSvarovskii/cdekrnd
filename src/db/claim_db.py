from src.database import get_async_session
from src.schemas import claim_schemas
from src.crud import claims_crud
# from src.utils import claim_utils as cust_utils


# async def add_new_user_to_database(
#     claim_data: claim_schemas.claimCreate
# ):
#     async for session in get_async_session():
#         await cust_utils.add_tg_user(
#             data=claim_data,
#             session=session
#         )
#         break


# async def get_claim(
#     user_id: int
# ):
#     async for session in get_async_session():
#         response = await claims_crud.crud_get_claim(
#             user_id=user_id,
#             session=session
#         )
#         break
#     return response
from typing import Union


async def create_claim(
    data: Union[claim_schemas.ClaimCreate, claim_schemas.ClaimCancelled],
):
    async for session in get_async_session():
        response = await claims_crud.crud_create_claim(
            data=data,
            session=session
        )
        break
    return response


async def create_claim_document(
    data: claim_schemas.ClaimDocumentCreate
):
    async for session in get_async_session():
        response = await claims_crud.crud_create_claim_document(
            data=data,
            session=session
        )
        break
    return response


async def get_claim_list_db(
    customer_id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_claim_list(
            customer_id=customer_id,
            session=session
        )
        break
    return response


async def get_viewed_claim_tickets_db(
    customer_id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_viewed_claim_tickets(
            customer_id=customer_id,
            session=session
        )
        break
    return response

async def get_claims_count_db(
    manager_user_id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_claims_count(
            manager_user_id=manager_user_id,
            session=session
        )
        break
    return response


async def get_cancelled_claims_count_db(
    manager_user_id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_cancelled_claims_count(
            manager_user_id=manager_user_id,
            session=session
        )
        break
    return response


async def get_claim_document_list_db(
    claim_id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_claim_document_list(
            claim_id=claim_id,
            session=session
        )
        break
    return response


async def get_one_claim_db(
    id: int
):
    async for session in get_async_session():
        response = await claims_crud.crud_get_one_claim(
            id=id,
            session=session
        )
        break
    return response


async def change_avail_claim(claim_id):
    async for session in get_async_session():
        await claims_crud.crud_change_avail_claim(
            claim_id=claim_id,
            session=session
        )
        break
    return {'status': 'ok'}
