from aiogram.filters.callback_data import CallbackData


class SupportCallbackFactory(
    CallbackData,
    prefix='sup',
    sep='_'
):
    id: int
    user_id: int


class SupportPageCallbackFactory(
    CallbackData,
    prefix='sup-pag',
    sep='_'
):
    page: int


class SupportViewedCallbackFactory(
    SupportCallbackFactory,
    prefix='sup-view',
    sep='_'
):
    pass


class SupportViewedPageCallbackFactory(
    SupportPageCallbackFactory,
    prefix='sup-pag-view',
    sep='_'
):
    pass
