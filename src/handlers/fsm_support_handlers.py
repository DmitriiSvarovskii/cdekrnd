# import aioredis
import json
import redis
# from redis import Redis

from aiogram import Bot, Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
# from aiogram.enums import ChatAction

from src.state import support_state as sup_state
from src.callbacks import SupportCallbackFactory
from src.db import customer_db, support_db, manager_db
from src.keyboards import support_kb, start_kb
from src.lexicons import customer_text, manager_text


router = Router(name=__name__)

# redis = Redis(name=__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
dispatcer = Dispatcher()
key = StorageKey(bot_id=5895760296, chat_id=5912814626, user_id=5912814626)


@router.callback_query(F.data == 'press_customer_support_chat')
async def process_support_call(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
):
    customer_data = await customer_db.get_customer(
        user_id=callback.message.chat.id
    )

    manager_data = await manager_db.get_manager_by_customer_id_db(
        customer_user_id=callback.message.chat.id
    )

    support_id = await support_db.create_support(customer_id=customer_data.id)

    await state.update_data(
        support_id=support_id,
        user_type='customer',
        manager_user_id=manager_data.user_id
    )

    await callback.message.answer(
        text=customer_text.support_cust_text['support_request_received'],
        reply_markup=support_kb.create_kb_close_support()
    )

    await bot.send_message(
        chat_id=manager_data.user_id,
        text=manager_text.support_request_message(callback.message.chat.id),
        reply_markup=await start_kb.create_kb_support_man_main(
            manager_data.user_id
        )
    )
    await state.set_state(sup_state.FSMSupport.waiting_for_manager_response)


@router.message(F.text == "Закрыть заявку")
async def process_finish_state(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    data = await state.get_data()

    if data['user_type'] == 'customer':
        manager_user_id = data['manager_user_id']
        await support_db.change_avail_support(support_id=data['support_id'])

        await bot.send_message(
            chat_id=manager_user_id,
            text=manager_text.support_manager_text['client_closed_ticket'],
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            chat_id=manager_user_id,
            text=manager_text.common_manager_text['main_menu'],
            reply_markup=await start_kb.create_kb_support_man_main(
                manager_user_id
            )
        )
        await message.answer(
            text=customer_text.support_cust_text['claim_closed'],
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            text=customer_text.common_cust_text['menu_item_selection'],
            reply_markup=await start_kb.create_kb_client()
        )
        r.delete(f"fsm:{manager_user_id}:{manager_user_id}:state")

        await state.clear()
    else:
        await message.answer(
            text=manager_text.support_manager_text['close_ticket_instr_remem'],
            reply_markup=support_kb.create_kb_close_support_manager()
        )


@router.message(sup_state.FSMSupport.waiting_for_manager_response)
async def process_message_client(
    message: Message,
    state: FSMContext,
):

    current_state = await state.get_data()
    await state.update_data(
        message_id=current_state.get(
            'message_id', []) + [message.message_id]
    )

    await state.set_state(sup_state.FSMSupport.waiting_for_manager_response)


@router.callback_query(SupportCallbackFactory.filter())
async def process_support_response(
    callback: CallbackQuery,
    callback_data: SupportCallbackFactory,
    state: FSMContext,
    bot: Bot
):
    print(await dispatcer.storage.get_data(key))

    await state.update_data(
        user_type='manager',
        customer_user_id=callback_data.user_id,
        support_id=callback_data.id
    )
    data = r.get(f'fsm:{callback_data.user_id}:{callback_data.user_id}:data')

    decoded_data = json.loads(data)
    message_id_list = decoded_data.get('message_id', [])

    await bot.send_message(
        chat_id=callback_data.user_id,
        text=customer_text.support_cust_text['manager_connected'],
        reply_markup=support_kb.create_kb_close_support()
    )
    if message_id_list:
        await bot.forward_messages(
            chat_id=callback.message.chat.id,
            from_chat_id=callback_data.user_id,
            message_ids=message_id_list
        )
    await callback.message.answer(
        text=manager_text.support_manager_text['close_ticket_instruction'],
        reply_markup=support_kb.create_kb_close_support_manager()
    )

    r.set(f"fsm:{callback_data.user_id}:{callback_data.user_id}:state",
          'FSMSupport:manager_response')

    await state.set_state(sup_state.FSMSupport.manager_response)


@router.message(sup_state.FSMSupport.manager_response)
async def process_message(
    message: Message,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()

    if data['user_type'] == 'manager':
        await bot.copy_message(
            chat_id=data['customer_user_id'],
            from_chat_id=message.from_user.id,
            message_id=message.message_id
        )

    elif data['user_type'] == 'customer':
        print(message.content_type)
        await bot.forward_message(
            chat_id=data['manager_user_id'],
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

    await state.set_state(sup_state.FSMSupport.manager_response)


@router.callback_query(F.data == "press_close_support")
async def process_finish_state_manager(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
):
    data = await state.get_data()

    if data['user_type'] == 'manager':
        await callback.message.delete()
        customer_user_id = data['customer_user_id']
        await support_db.change_avail_support(support_id=data['support_id'])

        await bot.send_message(
            chat_id=customer_user_id,
            text=customer_text.support_cust_text['manager_closed_claim'],
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            chat_id=customer_user_id,
            text=manager_text.common_manager_text['main_menu'],
            reply_markup=await start_kb.create_kb_client()
        )
        await callback.message.answer(
            text=manager_text.support_manager_text['ticket_closed'],
            reply_markup=await start_kb.create_kb_support_man_main(
                callback.message.chat.id
            )
        )
        r.delete(f"fsm:{customer_user_id}:{customer_user_id}:state")

        await state.clear()
    else:
        pass
