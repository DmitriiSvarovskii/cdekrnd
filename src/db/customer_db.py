from src.database import get_async_session
from src.schemas import customer_schemas
from src.crud import customer_crud as cust_crud
# from src.utils import customer_utils as cust_utils


# async def add_new_user_to_database(
#     customer_data: customer_schemas.CustomerCreate
# ):
#     async for session in get_async_session():
#         await cust_utils.add_tg_user(
#             data=customer_data,
#             session=session
#         )
#         break


async def get_customer_db(
    user_id: int
):
    async for session in get_async_session():
        response = await cust_crud.crud_get_customer(
            user_id=user_id,
            session=session
        )
        break
    return response


async def get_customer(
    user_id: int
):
    async for session in get_async_session():
        response = await cust_crud.crud_get_customer(
            user_id=user_id,
            session=session
        )
        break
    return response


async def get_customer_by_manag_id(
    manager_id: int
):
    async for session in get_async_session():
        response = await cust_crud.crud_get_customer_by_manag_id(
            manager_id=manager_id,
            session=session
        )
        break
    return response


async def create_customer_db(
    data: customer_schemas.CustomerCreate
):
    async for session in get_async_session():
        response = await cust_crud.crud_create_customer(
            data=data,
            session=session
        )
        break
    return response


async def create_customer(
    data: customer_schemas.CustomerCreate
):
    async for session in get_async_session():
        response = await cust_crud.crud_create_customer(
            data=data,
            session=session
        )
        break
    return response


async def update_customer(
    manager_id: int,
    user_id: int
):
    async for session in get_async_session():
        response = await cust_crud.crud_update_customer(
            manager_id=manager_id,
            user_id=user_id,
            session=session
        )
        break
    return response


async def update_customer_db(
    manager_id: int,
    user_id: int
):
    async for session in get_async_session():
        response = await cust_crud.crud_update_customer(
            manager_id=manager_id,
            user_id=user_id,
            session=session
        )
        break
    return response
