from aiogram.filters.callback_data import CallbackData


class ClaimDocumentCallbackFactory(
    CallbackData,
    prefix='cl-doc',
    sep='_'
):
    id: int


class ClaimCallbackFactory(
    CallbackData,
    prefix='cl',
    sep='_'
):
    id: int
    user_id: int


class ClaimPageCallbackFactory(
    CallbackData,
    prefix='cl-pag',
    sep='_'
):
    page: int


class ClaimtViewedCallbackFactory(
    CallbackData,
    prefix='cl-view',
    sep='_'
):
    pass


class ClaimtViewedPageCallbackFactory(
    CallbackData,
    prefix='cl-pag-view',
    sep='_'
):
    pass
