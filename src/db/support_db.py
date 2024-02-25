from src.database import get_async_session
from src.crud import support_crud


async def create_support(
    customer_id: int
):
    async for session in get_async_session():
        response = await support_crud.crud_create_support(
            customer_id=customer_id,
            session=session
        )
        break
    return response


async def get_support_list_db(
    customer_id: int
):
    async for session in get_async_session():
        response = await support_crud.crud_get_support_list(
            customer_id=customer_id,
            session=session
        )
        break
    return response


async def get_viewed_support_tickets_db(
    customer_id: int
):
    async for session in get_async_session():
        response = await support_crud.crud_get_viewed_support_tickets(
            customer_id=customer_id,
            session=session
        )
        break
    return response


async def change_avail_support(support_id):
    async for session in get_async_session():
        await support_crud.crud_change_avail_support(
            support_id=support_id,
            session=session
        )
        break
    return {'status': 'ok'}


async def get_supports_db(
    manager_user_id: int
):
    async for session in get_async_session():
        response = await support_crud.crud_get_supports_count(
            manager_user_id=manager_user_id,
            session=session
        )
        break
    return response
