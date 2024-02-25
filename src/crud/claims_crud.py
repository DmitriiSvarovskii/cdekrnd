from sqlalchemy import func
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.schemas import claim_schemas
from src.models import Claim, ClaimDocument, Customer, Manager

from typing import Union


async def crud_create_claim(
    data: Union[claim_schemas.ClaimCreate, claim_schemas.ClaimCancelled],
    session: AsyncSession,
):
    stmt = (
        insert(Claim).
        values(**data.model_dump()).
        returning(Claim.id)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar()


async def crud_create_claim_document(
    data: List[claim_schemas.ClaimDocumentCreate],
    session: AsyncSession,
):
    claim_documents = [ClaimDocument(**doc.model_dump()) for doc in data]
    session.add_all(claim_documents)
    await session.commit()
    return {"status": 201}


async def crud_get_claim_document_list(
    claim_id: int,
    session: AsyncSession,
) -> List[claim_schemas.ReadClaimDocument]:
    query = (
        select(ClaimDocument).
        where(ClaimDocument.claim_id == claim_id)
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def crud_get_claim_list(
    customer_id: int,
    session: AsyncSession,
) -> List[claim_schemas.ReadClaim]:
    query = (
        select(Claim).
        where(Claim.customer_id == customer_id,
              Claim.is_active)
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response


async def crud_get_viewed_claim_tickets(
    customer_id: int,
    session: AsyncSession,
) -> List[claim_schemas.ReadClaim]:
    query = (
        select(Claim).
        where(Claim.customer_id == customer_id,
              Claim.is_active.is_(False))
    )
    result = await session.execute(query)
    response = result.scalars().all()
    return response
# async def crud_get_claim_list(
#     customer_id: int,
#     session: AsyncSession,
# ) -> List[claim_schemas.ReadClaim]:
#     query = (
#         select(Claim).
#         where(Claim.customer_id == customer_id,
#               Claim.is_active)
#     )
#     result = await session.execute(query)
#     response = result.scalars().all()
#     return response


async def crud_get_one_claim(
    id: int,
    session: AsyncSession,
) -> Optional[claim_schemas.ReadClaim]:
    query = (
        select(Claim).
        where(Claim.id == id)
    )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def crud_change_avail_claim(
    claim_id: int,
    session: AsyncSession,
):
    stmt = (
        update(Claim)
        .where(
            Claim.id == claim_id,
        )
        .values(is_active=~Claim.is_active)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": "Претензия просмотрена закрыта"}


async def crud_get_claims_count(
    manager_user_id: int,
    session: AsyncSession
):
    query = (select(func.count(Claim.id))
             .join(Customer)
             .join(Manager)
             .where(Manager.user_id == manager_user_id,
                    Claim.is_active)
             )
    result = await session.execute(query)
    response = result.scalar()
    return response


async def crud_get_cancelled_claims_count(
    manager_user_id: int,
    session: AsyncSession
):
    query = (select(func.count(Claim.id))
             .join(Customer)
             .join(Manager)
             .where(Manager.user_id == manager_user_id,
                    Claim.completed.is_(False))
             )
    result = await session.execute(query)
    response = result.scalar()
    return response
