from aiogram.filters.state import State, StatesGroup


class FSMClaimsRegistration(StatesGroup):
    waybill_number = State()
    email_for_response = State()
    situation_description = State()
    required_amount = State()
    photos_or_scans = State()
    finished_claims = State()
