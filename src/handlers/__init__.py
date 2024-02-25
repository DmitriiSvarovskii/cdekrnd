__all__ = ("router",)

from aiogram import Router

from .start_handlers import router as start_router
from .claim_handlers import router as claim_router
from .common_handlers import router as common_router
from .fsm_claims_handlers import router as fsm_claim_router
from .fsm_register_manager import router as fsm_reg_man_router
from .fsm_support_handlers import router as fsm_support_router
from .fsm_waybill_handlers import router as fsm_wayllib_router
from .main_menu_handlers import router as main_menu_router
from .register_customer import router as reg_cust_router
from .support_handlers import router as support_router
from .unresolved_tickets_handler import router as unres_tick_router

router = Router(name=__name__)

router.include_routers(
    claim_router,
    start_router,
    fsm_claim_router,
    fsm_reg_man_router,
    fsm_support_router,
    fsm_wayllib_router,
    main_menu_router,
    reg_cust_router,
    support_router,
    unres_tick_router,
)

router.include_router(common_router)
# from aiogram import Router, F
# from aiogram.filters import CommandStart

# # from .start_handlers import process_start_command
# from .fsm_waybill_handlers import (
#     process_cargo_description,
#     process_cargo_weight,
#     process_cargo_dimensions,
#     process_departure_address,
#     process_destination_address,
#     process_payment_method,
#     process_create_waybill,
#     process_cancel_waybill,
# )
# from .fsm_claims_handlers import (
#     process_waybill_number,
#     process_email_for_response,
#     process_situation_description,
#     process_required_amount,
#     process_photos_or_scans,
#     process_claim_registration,
#     process_photos_or_scans_test,
#     process_cancel_claim,
# )
# from .fsm_support_handlers import (
#     process_support_call,
#     process_message,
#     process_support_response,
#     process_finish_state,
#     process_message_client,
#     process_finish_state_manager,
# )
# from .main_menu_handlers import (
#     process_support_list,
#     process_support_list_next_page,
#     process_viewed_support_tickets,
#     process_claim_list,
#     process_claim_list_next_page,
#     process_one_claim,
#     process_claim_document,
#     process_main_menu_manager,
#     process_viewed_claim_tickets,
#     process_viewed_support_tickets_next_page,
#     process_view_unresolved_tickets,
# )
# from .common_handlers import process_pass
# from .fsm_register_manager import (
#     request_registration_code,
#     process_admin_password_attempt,
#     process_cancel_registration_manager,
# )
# from .register_customer import (
#     process_register_customer
# )
# from src.callbacks import (
#     SupportCallbackFactory,
#     SupportPageCallbackFactory,
#     ClaimCallbackFactory,
#     ClaimPageCallbackFactory,
#     ClaimDocumentCallbackFactory,
#     SupportViewedCallbackFactory,
#     SupportViewedPageCallbackFactory,
#     ClaimtViewedCallbackFactory
# )

# from src.state import (
#     claims_state as claims,
#     waybill_state,
#     support_state,
#     manager_registration_state
# )


# def register_user_commands(router: Router) -> None:
# router.message.register(
#     process_start_command, CommandStart()
# )
# router.message.register(
#     process_cancel_waybill,
#     F.text == "Отменить регистрацию накладной"
# )
# router.callback_query.register(
#     process_cargo_description, F.data == 'press_register_waybill'
# )
# router.message.register(
#     process_cargo_weight,
#     waybill_state.FSMCreateWaybill.cargo_description
# )
# router.message.register(
#     process_cargo_dimensions,
#     waybill_state.FSMCreateWaybill.cargo_weight_kg
# )
# router.message.register(
#     process_departure_address,
#     waybill_state.FSMCreateWaybill.cargo_dimensions
# )
# router.message.register(
#     process_destination_address,
#     waybill_state.FSMCreateWaybill.departure_address
# )
# router.message.register(
#     process_payment_method,
#     waybill_state.FSMCreateWaybill.delivery_address
# )
# router.message.register(
#     process_create_waybill,
#     waybill_state.FSMCreateWaybill.payment_method
# )

# router.callback_query.register(
#     process_waybill_number, F.data == 'press_register_complaint'
# )
# router.message.register(
#     process_cancel_claim,
#     F.text == "Отменить заполнение претензии"
# )
# router.message.register(
#     process_email_for_response,
#     claims.FSMClaimsRegistration.waybill_number
# )
# router.message.register(
#     process_situation_description,
#     claims.FSMClaimsRegistration.email_for_response
# )
# router.message.register(
#     process_required_amount,
#     claims.FSMClaimsRegistration.situation_description
# )
# router.message.register(
#     process_photos_or_scans,
#     claims.FSMClaimsRegistration.required_amount
# )
# router.message.register(
#     process_photos_or_scans_test,
#     claims.FSMClaimsRegistration.photos_or_scans,
#     F.photo | F.document | F.media_group
# )
# router.message.register(
#     process_claim_registration,
#     F.text == 'Отправить претензию'
# )

# router.callback_query.register(
#     process_support_call, F.data == 'press_customer_support_chat'
# )
# router.callback_query.register(
#     process_support_response,
#     SupportCallbackFactory.filter(),
# )
# router.message.register(
#     process_finish_state,
#     F.text == "Закрыть заявку"
# )
# router.callback_query.register(
#     process_finish_state_manager,
#     F.data == "press_close_support"
# )
# router.message.register(
#     process_message_client,
#     support_state.FSMSupport.waiting_for_manager_response,
# )
# router.message.register(
#     process_message,
#     support_state.FSMSupport.manager_response,
# )

# router.callback_query.register(
#     process_support_list,
#     F.data == 'press_support_list'
# )

# router.callback_query.register(
#     process_support_list_next_page,
#     SupportPageCallbackFactory.filter(),
# )

# router.callback_query.register(
#     process_claim_list,
#     F.data == 'press_claims_list'
# )

# router.callback_query.register(
#     process_claim_list_next_page,
#     ClaimPageCallbackFactory.filter(),
# )

# router.callback_query.register(
#     process_one_claim,
#     ClaimCallbackFactory.filter()
# )
# router.callback_query.register(
#     process_claim_document,
#     ClaimDocumentCallbackFactory.filter(),
# )

# router.message.register(
#     send_echo
# )
# router.callback_query.register(
#     request_registration_code, F.data == 'press_register_manager'
# )
# router.message.register(
#     process_cancel_claim,
#     F.text == "Отменить заполнение претензии"
# )

# router.callback_query.register(
#     process_register_customer, F.data == 'press_register_customer'
# )
# router.message.register(
#     process_cancel_registration_manager, F.text == 'Отменить регистрацию'
# )
# router.message.register(
#     process_admin_password_attempt,
#     manager_registration_state.FSMManagerRegistration.counter
# )

# router.callback_query.register(
#     process_main_menu_manager, F.data == 'press_main_menu_manager'
# )

# router.callback_query.register(
#     process_viewed_support_tickets, F.data == 'press_viewed_supports'
# )
# router.callback_query.register(
#     process_viewed_support_tickets_next_page,
#     SupportViewedPageCallbackFactory.filter(),
# )

# router.callback_query.register(
#     process_viewed_claim_tickets, F.data == 'press_viewed_claims'
# )

# router.callback_query.register(
#     process_view_unresolved_tickets, F.data == 'view_unresolved_tickets'
# )
# router.callback_query.register(
#     process_pass, F.data == 'press_pass'
# )
