from typing import Union, Optional
from aiogram.types import CallbackQuery
from aiogram.types import Message

from src.schemas import customer_schemas, manager_schemas
from src.db import manager_db, customer_db


async def initialize_user_session(message: Message):
    user_data = await manager_db.get_manager_db(
        user_id=message.chat.id,
    )
    if user_data:
        return {'message': 'manager'}

    else:
        customer_data = await customer_db.get_customer_db(
            user_id=message.chat.id,
        )
        if customer_data:
            bot_param = await get_manager_id(text=message.text)
            if bot_param:
                await customer_db.update_customer_db(manager_id=bot_param,
                                                     user_id=message.chat.id)
                return {'message': 'client'}
            return {'message': 'client'}
        else:
            bot_param = await get_manager_id(text=message.text)
            print(bot_param)
            if bot_param:
                data = await create_new_customer_data(
                    event=message,
                    manager_id=bot_param
                )
                await customer_db.create_customer_db(data=data)
                return {'message': 'client'}
            return None


async def get_manager_id(
    text: str
) -> Optional[int]:
    if text.strip() == "/start":
        return None
    else:
        manager_user_id = text.replace("/start", "").strip()
        if manager_user_id:
            try:
                manager_id = int(manager_user_id)
            except ValueError:
                return None
            else:
                manager_data = await manager_db.get_manager_db(
                    user_id=manager_id,
                )
                print(manager_data)
                if manager_data:
                    return manager_data.id
        return None


async def create_manager(
    message: Message
):
    data = await create_manager_data(message=message)
    print(data)
    await manager_db.create_manager_db(data=data)
    return {'message': 'success'}


async def create_manager_data(
    message: Message
) -> Optional[manager_schemas.ManagerCreate]:
    manager_data = manager_schemas.ManagerCreate(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    return manager_data


async def create_customer(
    callback: CallbackQuery
):
    manager_id = await get_manager_id(text=callback.message.text)

    data = await create_new_customer_data(
        event=callback,
        manager_id=manager_id
    )
    await customer_db.create_customer_db(data=data)
    return {'message': 'success'}


async def create_new_customer_data(
    event: Union[CallbackQuery, Message],
    manager_id: Optional[int] = None
) -> Optional[customer_schemas.CustomerCreate]:
    if isinstance(event, CallbackQuery):
        user = event.message.chat
    elif isinstance(event, Message):
        user = event.chat

    customer_data = customer_schemas.CustomerCreate(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        manager_id=manager_id
    )
    return customer_data
