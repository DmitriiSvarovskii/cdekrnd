from sqlalchemy import func
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.schemas import waybill_schemas
from src.models import Waybill, ClaimDocument, Customer, Manager

from typing import Union


async def crud_create_waybill(
    data: Union[waybill_schemas.WaybillCreate,
                waybill_schemas.WaybillCancelled],
    session: AsyncSession,
):
    stmt = (
        insert(Waybill).
        values(**data.model_dump()).
        returning(Waybill.id)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


async def crud_get_cancelled_waybill_count(
    manager_user_id: int,
    session: AsyncSession
):
    query = (select(func.count(Waybill.id))
             .join(Customer)
             .join(Manager)
             .where(Manager.user_id == manager_user_id,
                    Waybill.completed.is_(False))
             )
    result = await session.execute(query)
    response = result.scalar()
    return response
