from aiogram.filters.state import State, StatesGroup


class FSMCreateWaybill(StatesGroup):
    cargo_description = State()
    cargo_weight_kg = State()
    cargo_dimensions = State()
    departure_address = State()
    delivery_address = State()
    payment_method = State()
