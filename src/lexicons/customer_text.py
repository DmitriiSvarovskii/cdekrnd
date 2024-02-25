from src.schemas import waybill_schemas


claims_cust_text: dict[str, str] = {
    'waybill_number': 'Номер накладной',
    'email_for_response': 'e-mail для ответа на претензию',
    'situation_description': 'описание ситуации',
    'required_amount': 'требуемая сумма',
    'photos_or_scans': 'фото/сканы',
    'claim_interruption': 'Вы прервали заполнение претензии',
    'claim_registered': 'Претензия зарегестрирована',
}

claims_cust_btn: dict[str, str] = {
    'cancel_claim_filling': 'Отменить заполнение претензии',
    'submit_claim': 'Отправить претензию',
}

common_cust_text: dict[str, str] = {
    'main_menu': 'Главное меню',
    'menu_item_selection': 'Выберите пункт меню',
}

support_cust_text: dict[str, str] = {
    "support_request_received": "Вы обратились в поддержку, ожидайте ответа "
                                "менеджера.\nДля завершения заявки нажмите "
                                "кнопку 'Закрыть заявку'",
    "claim_closed": "Заявка закрыта",
    "manager_connected": "Менеджер подключился к чату",
    "manager_closed_claim": "Менеджер закрыл заявку",
    "claim_closed_btn": "Закрыть заявку"
}


wayllib_cust_text: dict[str, str] = {
    'cargo_description': 'Описание груза',
    'cargo_weight': 'Вес груза (кг)',
    'cargo_dimensions': 'Габариты груза',
    'departure_address': 'Точный адрес отправки',
    'delivery_address': 'Точный адрес получения',
    'payment_method': 'Способ оплаты',
    'waybill_created': 'Ваша накладная создана',
    'waybill_creat_cancell': 'Вы отменили создание накладной'
}

registration_cust_text: dict[str, str] = {
    'registration_completed': 'Регистрация завершена. '
                              'Добро пожаловать в наше сообщество!'
}

main_client_dict: dict[str, dict[str, str]] = {
    "register_waybill": {
        "text": "Зарегистрировать накладную",
        "callback_data": "press_register_waybill"
    },
    "register_complaint": {
        "text": "Зарегистрировать жалобу",
        "callback_data": "press_register_complaint"
    },
    "customer_support_chat": {
        "text": "Чат-поддержка",
        "callback_data": "press_customer_support_chat"
    }
}


async def create_waybill_text(data: waybill_schemas.WaybillBase) -> str:
    text = (
        f'Описание груза:\n{data.cargo_description}'
        f'\nВес груза: {data.cargo_weight_kg}'
        f'\nГабаритыгруза:'
        f'\n- длина:{data.cargo_length}'
        f'\n- ширина:{data.cargo_width}'
        f'\n- высота:{data.cargo_height}'
        f'\nТочный адрес отправки: {data.departure_address}'
        f'\nТочный адрес полученя: {data.destination_address}'
        f'\nСпособ оплаты: {data.payment_method}'
    )
    return text
