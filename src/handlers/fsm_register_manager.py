from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.lexicons import manager_text
from src.state import manager_registration_state as man_state
from src.keyboards import start_kb
from src.config import settings
from src.utils import user_utils

router = Router(name=__name__)


@router.callback_query(F.data == 'press_register_manager')
async def request_registration_code(
    calback: CallbackQuery,
    state: FSMContext
):
    await calback.message.answer(
        text=manager_text_manager_text['input_code'],
        reply_markup=start_kb.create_kb_register_manager()
    )

    await state.set_state(man_state.FSMManagerRegistration.counter)


@router.message(man_state.FSMManagerRegistration.counter)
async def process_admin_password_attempt(
    message: Message,
    state: FSMContext,
):
    pass_admin_attempts_key = 'pass_admin_attempts'
    max_attempts = 3

    if message.text == settings.PASS_ADMIN:
        await user_utils.create_manager(message=message)
        await message.answer(
            text=manager_text_manager_text['successful_registration'],
            reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            text=manager_text.common_manager_text['main_menu'],
            reply_markup=await start_kb.create_kb_support_man_main(
                message.chat.id
            )
        )
        await state.clear()
    else:
        attempts = await state.get_data() or {pass_admin_attempts_key: 0}
        current_attempts = attempts.get(pass_admin_attempts_key, 0)

        current_attempts += 1

        await state.update_data({pass_admin_attempts_key: current_attempts})

        if current_attempts >= max_attempts:
            await state.clear()
            await message.answer(
                text=manager_text_manager_text['exceeded_pass_att'],
                reply_markup=ReplyKeyboardRemove()
            )
            await message.answer(
                text=manager_text_manager_text['reg_method_select'],
                reply_markup=await start_kb.create_kb_register_user()
            )
        else:
            await message.answer(
                text=manager_text_manager_text['incorrect_password']
            )


@router.message(F.text == 'Отменить регистрацию')
async def process_cancel_registration_manager(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        text=manager_text_manager_text['registration_cancelled'],
        reply_markup=await start_kb.create_kb_register_user()
    )
    await state.clear()
