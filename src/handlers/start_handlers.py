from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards import start_kb
from src.utils import user_utils
from src.lexicons import registration_text

router = Router(name=__name__)


@router.message(CommandStart())
async def process_start_command(message: Message):
    print(message.chat.id)
    user_info = await user_utils.initialize_user_session(message=message)
    if user_info and user_info['message'] == 'manager':
        await message.answer(
            text='Manager',
            reply_markup=await start_kb.create_kb_support_man_main(
                message.chat.id
            )
        )
    elif user_info and user_info['message'] == 'client':
        await message.answer(
            text='Client',
            reply_markup=await start_kb.create_kb_client()
        )
    else:
        await message.answer(
            text=registration_text.welcome_message['text'],
            reply_markup=await start_kb.create_kb_register_user()
        )
