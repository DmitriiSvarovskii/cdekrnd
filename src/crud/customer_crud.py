from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.schemas import customer_schemas
from src.models import Customer


async def crud_get_customer(
    user_id: int,
    session: AsyncSession,

) -> Optional[customer_schemas.ReadCustomer]:
    query = (
        select(Customer).
        where(Customer.user_id == user_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def crud_get_customer_by_manag_id(
    manager_id: int,
    session: AsyncSession,

) -> Optional[customer_schemas.ReadCustomer]:
    query = (
        select(Customer).
        where(Customer.manager_id == manager_id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def crud_create_customer(
    data: customer_schemas.CustomerCreate,
    session: AsyncSession,
):
    stmt = (
        insert(Customer).
        values(**data.model_dump())
    )
    print('tyt')
    await session.execute(stmt)
    await session.commit()
    return {"status": 201}


async def crud_update_customer(
    manager_id: int,
    user_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Customer).
        where(Customer.user_id == user_id).
        values(manager_id=manager_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 200}
