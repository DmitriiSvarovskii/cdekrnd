from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.types import (
    Message,
    BufferedInputFile,
    CallbackQuery,
    ReplyKeyboardRemove
)

from src.db import customer_db, manager_db, waybill_db
from src.state import waybill_state as way_state
from src.schemas import waybill_schemas
from src.utils.create_pdf import create_pdf
from src.lexicons import customer_text, manager_text
from src.keyboards import wayllib_kb, start_kb

router = Router(name=__name__)


@router.callback_query(F.data == 'press_register_waybill')
async def process_cargo_description(
    calback: CallbackQuery,
    state: FSMContext
):
    await calback.message.answer(
        text=customer_text.wayllib_cust_text['cargo_description'],
        reply_markup=wayllib_kb.create_kb_close_wayllib()
    )
    await state.set_state(way_state.FSMCreateWaybill.cargo_description)


@router.message(way_state.FSMCreateWaybill.cargo_description)
async def process_cargo_weight(
    message: Message,
    state: FSMContext,
):
    await state.update_data(cargo_description=message.text)
    await message.answer(text=customer_text.wayllib_cust_text['cargo_weight'],
                         reply_markup=wayllib_kb.create_kb_close_wayllib())
    await state.set_state(way_state.FSMCreateWaybill.cargo_weight_kg)


@router.message(way_state.FSMCreateWaybill.cargo_weight_kg)
async def process_cargo_dimensions(
    message: Message,
    state: FSMContext,
):
    await state.update_data(cargo_weight_kg=message.text)
    await message.answer(
        text=customer_text.wayllib_cust_text['cargo_dimensions'],
        reply_markup=wayllib_kb.create_kb_close_wayllib()
    )
    await state.set_state(way_state.FSMCreateWaybill.cargo_dimensions)


@router.message(way_state.FSMCreateWaybill.cargo_dimensions)
async def process_departure_address(
    message: Message,
    state: FSMContext,
):
    cargo_data = message.text.split("-")

    await state.update_data(
        cargo_length=cargo_data[0],
        cargo_width=cargo_data[1],
        cargo_height=cargo_data[2]
    )
    await message.answer(
        text=customer_text.wayllib_cust_text['departure_address'],
        reply_markup=wayllib_kb.create_kb_close_wayllib()
    )
    await state.set_state(way_state.FSMCreateWaybill.departure_address)


@router.message(way_state.FSMCreateWaybill.departure_address)
async def process_destination_address(
    message: Message,
    state: FSMContext,
):
    await state.update_data(departure_address=message.text)
    await message.answer(
        text=customer_text.wayllib_cust_text['delivery_address'],
        reply_markup=wayllib_kb.create_kb_close_wayllib()
    )
    await state.set_state(way_state.FSMCreateWaybill.delivery_address)


@router.message(way_state.FSMCreateWaybill.delivery_address)
async def process_payment_method(
    message: Message,
    state: FSMContext,
):
    await state.update_data(destination_address=message.text)
    await message.answer(
        text=customer_text.wayllib_cust_text['payment_method'],
        reply_markup=wayllib_kb.create_kb_close_wayllib()
    )
    await state.set_state(way_state.FSMCreateWaybill.payment_method)


@router.message(way_state.FSMCreateWaybill.payment_method)
async def process_create_waybill(
    message: Message,
    state: FSMContext
):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await state.update_data(payment_method=message.text)
    await message.answer(
        text=customer_text.wayllib_cust_text['waybill_created'],
        reply_markup=ReplyKeyboardRemove()
    )
    customer_data = await customer_db.get_customer(user_id=message.chat.id)
    await state.update_data(customer_id=customer_data.id)
    data = await state.get_data()

    waybill_data = waybill_schemas.WaybillCreate(**data)

    wayllib_id = await waybill_db.create_waybill_db(data=waybill_data)

    text_pdf = await customer_text.create_waybill_text(data=waybill_data)

    pdf = create_pdf(text_pdf)

    await message.answer_document(
        document=BufferedInputFile(
            file=pdf,
            filename=f'Накладная №{wayllib_id}.pdf'
        )
    )
    await message.answer(
        text=customer_text.common_cust_text['menu_item_selection'],
        reply_markup=await start_kb.create_kb_client()
    )

    await state.clear()


@router.message(F.text == "Отменить регистрацию накладной")
async def process_cancel_waybill(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    customer_data = await customer_db.get_customer(user_id=message.chat.id)

    manager_data = await manager_db.get_manager_by_id(
        id=customer_data.manager_id
    )
    await state.update_data(customer_id=customer_data.id)
    data = await state.get_data()
    waybill_data = waybill_schemas.WaybillCancelled(**data)
    await waybill_db.create_waybill_db(data=waybill_data)

    await bot.send_message(
        chat_id=manager_data.user_id,
        text=manager_text.wayllib_manager_text['registration_interrupted'],
        reply_markup=ReplyKeyboardRemove()
    )
    await bot.send_message(
        chat_id=manager_data.user_id,
        text=manager_text.common_manager_text['main_menu'],
        reply_markup=await start_kb.create_kb_support_man_main(
            manager_data.user_id)
    )

    await message.answer(
        text=customer_text.wayllib_cust_text['waybill_creat_cancell'],
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        text=customer_text.common_cust_text['menu_item_selection'],
        reply_markup=await start_kb.create_kb_client()
    )

    await state.clear()


# ошибка ввода
# async def warning_not_location(message: Message):
#     await message.answer(
#         text=LEXICON_RU['error_location'],
#         reply_markup=delivery_keyboards.create_kb_delivery_fsm()
#     )
