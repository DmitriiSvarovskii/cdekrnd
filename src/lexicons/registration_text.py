register_new_user: dict[str, dict[str, str]] = {
    "register_customer": {
        "text": "Зарегестрироваться как клиент",
        "callback_data": "press_register_customer"
    },
    "register_manager": {
        "text": "Зарегестрироваться как менеджер",
        "callback_data": "press_register_manager"
    }
}


cancel_registr_txt: dict[str, str] = {
    'cancel_registration': 'отменить регистрацию'}


welcome_message: dict[str, str] = {
    "text": 'Добро пожаловать!\n'
            'Я бот-помощник транспортной компании '
            'СДЕК-Ростов-на-Дону.\n\n'
            'Выберите, пожалуйста, вариант регистрации:\n'
            '1. Клиент\n'
            '2. Менеджер'
}
