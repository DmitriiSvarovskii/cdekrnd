from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.models import Support
from src.schemas import support_schemas
from sqlalchemy import func
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.schemas import claim_schemas
from src.models import Claim, Customer, Manager


async def crud_create_support(
    customer_id: int,
    session: AsyncSession,
):
    stmt = (
        insert(Support).
        values(customer_id=customer_id).
        returning(Support.id)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


async def crud_get_support_list(
    customer_id: int,
    session: AsyncSession,
) -> List[support_schemas.ReadSupport]:
    query = (
        select(Support).
        where(Support.customer_id == customer_id,
              Support.is_active)
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def crud_get_viewed_support_tickets(
    customer_id: int,
    session: AsyncSession,
) -> List[support_schemas.ReadSupport]:
    query = (
        select(Support).
        where(Support.customer_id == customer_id,
              Support.is_active.is_(False))
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def crud_change_avail_support(
    support_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Support)
        .where(
            Support.id == support_id,
        )
        .values(is_active=~Support.is_active)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Заявка закрыта"}


async def crud_get_supports_count(
    manager_user_id: int,
    session: AsyncSession
):
    query = (select(func.count(Support.id))
             .join(Customer)
             .join(Manager)
             .where(Manager.user_id == manager_user_id,
                    Support.is_active)
             )
    result = await session.execute(query)
    response = result.scalar()
    return response
