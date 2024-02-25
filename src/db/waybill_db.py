from src.database import get_async_session
from src.schemas import waybill_schemas
from src.crud import waybill_crud

from typing import Union


async def create_waybill_db(
    data: Union[waybill_schemas.WaybillCreate,
                waybill_schemas.WaybillCancelled],
):
    async for session in get_async_session():
        response = await waybill_crud.crud_create_waybill(
            data=data,
            session=session
        )
        break
    return response


async def get_cancelled_waybill_count_db(
    manager_user_id: int
):
    async for session in get_async_session():
        response = await waybill_crud.crud_get_cancelled_waybill_count(
            manager_user_id=manager_user_id,
            session=session
        )
        break
    return response
