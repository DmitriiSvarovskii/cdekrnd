from aiogram.types import Message
from typing import Optional, Any

from src.models import Customer
from src.schemas import customer_schemas
from src.db import manager_db, customer_db


async def initialize_user_session(message: Message):
    data = await check_manager(user_id=message.chat.id)
    if data:
        return {'message': 'admin'}
    else:
        customer = await customer_db.get_customer(
            user_id=message.chat.id
        )

        customer_data = await create_customer_data_from_message(
            message=message
        )
        if customer:
            if not compare_customer_data(customer, customer_data):
                await customer_db.update_customer(
                    data=customer_data,
                )
                return {'message': 'customer'}
        else:
            await customer_db.create_customer(
                data=customer_data,
            )
            return {'message': 'customer'}


async def check_manager(user_id: int):
    data = await manager_db.get_manager(
        user_id=user_id,
    )
    return data


def compare_customer_data(
    customer: Customer,
    data: customer_schemas.CustomerCreate
) -> bool:
    return (
        customer and
        customer.first_name == data.first_name and
        customer.last_name == data.last_name and
        customer.username == data.username  # and
        # customer.manager_id == data.manager_id
    )


async def get_manager_id(
    message: Message
) -> Any:
    if message.text.strip() == "/start":
        return None
    else:
        manager_user_id = message.text.replace("/start", "").strip()
        if manager_user_id:
            manager_data = await manager_db.get_manager(
                user_id=int(manager_user_id),
            )
            if manager_data:
                return manager_data.id
        return None


async def create_customer_data_from_message(
    message: Message
) -> Optional[customer_schemas.CustomerCreate]:
    manager_id = await get_manager_id(message=message)

    customer_data = customer_schemas.CustomerCreate(
        user_id=message.from_user.id,
        manager_id=manager_id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username
    )
    return customer_data


async def add_tg_user(
        data: customer_schemas.CustomerCreate
):
    try:
        customer = await customer_db.get_customer(
            user_id=data.user_id
        )

        if customer:
            if not compare_customer_data(customer, data):
                await customer_db.update_customer(
                    data=data,
                )
            return customer
        else:
            created_customer = await customer_db.create_customer(
                data=data,
            )
            return created_customer
    except Exception:
        return None
