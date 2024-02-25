from src.database import get_async_session
from src.schemas import customer_schemas, manager_schemas
from src.crud import manager_crud
from src.utils import customer_utils as cust_utils


async def add_new_user_to_database(
    customer_data: customer_schemas.CustomerCreate
):
    async for session in get_async_session():
        await cust_utils.add_tg_user(
            data=customer_data,
            session=session
        )
        break


async def create_manager_db(
    data: manager_schemas.ManagerCreate
):
    async for session in get_async_session():
        await manager_crud.crud_create_manager(
            data=data,
            session=session
        )
        break


async def get_manager(
    user_id: int
):
    async for session in get_async_session():
        response = await manager_crud.crud_get_manager(
            user_id=user_id,
            session=session
        )
        break
    return response


async def get_manager_by_customer_id_db(
    customer_user_id: int
):
    async for session in get_async_session():
        response = await manager_crud.crud_get_manager_by_customer_id(
            customer_user_id=customer_user_id,
            session=session
        )
        break
    return response


async def get_manager_db(
    user_id: int
):
    async for session in get_async_session():
        response = await manager_crud.crud_get_manager(
            user_id=user_id,
            session=session
        )
        break
    return response


# async def get_manager_db(
#     user_id: int
# ):
#     async for session in get_async_session():
#         response = await manager_crud.crud_get_manager(
#             user_id=user_id,
#             session=session
#         )
#         break
#     return response


async def get_manager_by_id(
    id: int
):
    async for session in get_async_session():
        response = await manager_crud.crud_get_manager_by_id(
            id=id,
            session=session
        )
        break
    return response
