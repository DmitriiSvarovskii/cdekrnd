from src.db import support_db, customer_db, manager_db


async def get_support_list(user_id: int):
    manager_data = await manager_db.get_manager(user_id=user_id)
    customer_data = await customer_db.get_customer_by_manag_id(
        manager_id=manager_data.id)
    support_list = await support_db.get_support_list_db(
        customer_id=customer_data.id
    )
    return support_list, customer_data.user_id


async def get_viewed_support_tickets(user_id: int):
    manager_data = await manager_db.get_manager(user_id=user_id)
    customer_data = await customer_db.get_customer_by_manag_id(
        manager_id=manager_data.id)
    support_list = await support_db.get_viewed_support_tickets_db(
        customer_id=customer_data.id
    )
    return support_list, customer_data.user_id
