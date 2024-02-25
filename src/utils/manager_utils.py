from src.schemas import manager_schemas
from src.db import claim_db, support_db, waybill_db


async def get_manager_data(user_id: int):
    supports_count_active = await support_db.get_supports_db(user_id)
    claims_count_activ = await claim_db.get_claims_count_db(user_id)
    claim_count_cancell = await claim_db.get_cancelled_claims_count_db(user_id)
    waybill_count_cancell = await waybill_db.get_cancelled_waybill_count_db(user_id)
    count_cancelled = waybill_count_cancell + claim_count_cancell

    manager_data = manager_schemas.ReadManagerMainText(
        supports_count_active=supports_count_active,
        claims_count_activ=claims_count_activ,
        count_cancelled=count_cancelled
    )

    return manager_data


async def get_unresolved_tickets_data(user_id: int):
    claim_count_cancell = await claim_db.get_cancelled_claims_count_db(user_id)
    waybill_count_cancell = await waybill_db.get_cancelled_waybill_count_db(user_id)
    return claim_count_cancell, waybill_count_cancell
