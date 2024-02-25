from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.schemas import manager_schemas
from src.models import Manager, Customer


async def crud_get_manager(
    user_id: int,
    session: AsyncSession,
) -> Optional[manager_schemas.ManagerInfo]:
    query = (
        select(Manager)
        .filter(Manager.user_id == user_id)
    )
    result = await session.execute(query)
    manager = result.scalar()
    return manager


async def crud_get_manager_by_id(
    id: int,
    session: AsyncSession,
) -> Optional[manager_schemas.ManagerInfo]:
    query = (
        select(Manager)
        .filter(Manager.id == id)
    )
    result = await session.execute(query)
    manager = result.scalar()
    return manager


async def crud_create_manager(
    data: manager_schemas.ManagerCreate,
    session: AsyncSession,
):
    stmt = (
        insert(Manager).
        values(**data.model_dump())
    )
    print('tyt')
    await session.execute(stmt)
    await session.commit()
    return {"status": 201}


async def crud_get_manager_by_customer_id(
    customer_user_id: int,
    session: AsyncSession
):
    query = (select(Manager)
             .join(Customer)
             .filter(Customer.user_id == customer_user_id)
             )
    result = await session.execute(query)
    manager = result.scalar()
    return manager
