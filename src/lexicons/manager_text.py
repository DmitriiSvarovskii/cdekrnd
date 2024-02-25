from typing import Optional

from src.schemas import manager_schemas, claim_schemas


claims_manager_text: dict[str, str] = {
    'new_claim_registered': 'Зарегестрирована новая претензия',
    'claim_interrupted': 'Клиент прервал заполнение претензии',
    'viewed_claims': 'Просмотренные претензии',
    'new_claims': 'Новые претензии',
    'claims_list': 'Список претензий',
    'missing_photos_documents': 'Фото/документы отсутствуют',
    'forward': '>>',
    'backward': '<<',
    'photos_documents': "Фото/документы претензии",
}


common_manager_text: dict[str, str] = {
    'main_menu': 'Главное меню',
    'unprocessed_inquiries': 'Необработанные обращения',
    'invalid_request_message': 'некорректный запрос',
}

register_manager_text: dict[str, str] = {
    'input_code': 'Введите код для регистрации. '
                  'Для отмены регистрации, нажмите "отмена регистрации',
    'successful_registration': 'Вы успешно зарегестрировались',
    'exceeded_pass_att': 'Превышено количество попыток ввода пароля.',
    'reg_method_select': 'Выберите способ регистрации',
    'incorrect_password': 'Вы ввели неверный пароль. Попробуйте еще раз',
    'registration_cancelled': 'Вы отменили регистрацию',
}

support_manager_text: dict[str, str] = {
    'client_closed_ticket': 'Клиент закрыл заявку',
    'close_ticket_instruction': 'Для завершения заявки нажмите '
                                'кнопку "Закрыть заявку"',
    'ticket_closed': 'Заявка закрыта.\nВыберите пункт меню',
    'support_requests': 'Заявки на поддержку',
    'viewed_support_requests': 'Просмотренные заявки на поддержку',
    'close_ticket_instr_remem': 'Для завершения заявки нажмите кнопку '
                               '"Закрыть заявку", отправленную '
                               'Вам при принятии заявки',
    'archive': 'Архив',
    'new_supports': 'Новые заявки',
    "claim_closed_btn": "Закрыть заявку"

}


wayllib_manager_text: dict[str, str] = {
    'registration_interrupted': 'Клиент прервал регистрацию накладной',
}

support_manager_btn: dict[str, dict[str, str]] = {
    "accept": {
        "text": "Начать беседу",
        "callback_data": "press_support_man"
    }
}


async def create_claim_text(
    data: claim_schemas.ClaimBase,
    customer_user_id: Optional[int] = None
) -> str:
    text = (
        f'<a href="tg://user?id={customer_user_id}">Ссылка на клиента</a>\n'
        f'Номер накладной:{data.waybill_number}'
        f'\nemail: {data.email_for_response}'
        f'\nОписание проблемы: {data.situation_description}'
        f'\nСумма ущерба: {data.required_amount}'
    )
    return text


def support_request_message(user_id: int) -> str:
    return (
        'Клиент обратился в поддержку '
        f'<a href="tg://user?id={user_id}">Ссылка на клиента</a>'
    )


def support_list_btn_message(
    user_id: int,
    support_id: int,
) -> str:
    return (
        f'Заявка №{support_id} от клиента №{user_id}')


async def create_manager_main_btn(
    data: manager_schemas.ReadManagerMainText,
) -> dict:
    button_text = {
        "support": {
            "text": f"Чаты с клиентами. Новые({data.supports_count_active})",
            "callback_data": "press_support_list"
        },
        "claim": {
            "text": "Претензии от клиентов. "
                    f"Новые ({data.claims_count_activ})",
            "callback_data": "press_claims_list"
        },
        "unresolved_tickets": {
            "text": f"Незавершенные обращения. Новые ({data.count_cancelled})",
            "callback_data": "view_unresolved_tickets"
        }
    }
    return button_text


async def create_manager_unresolved_tickets_btn(
    claims: int,
    wayllib: int,
) -> dict:
    button_text = {
        "wayllib": {
            "text": f"Незавершенные накладные. Новые({wayllib})",
            "callback_data": "press_support_list"
        },
        "claim": {
            "text": f"Незавершенные претензии. Новые ({claims})",
            "callback_data": "press_claims_list"
        },
    }
    return button_text
