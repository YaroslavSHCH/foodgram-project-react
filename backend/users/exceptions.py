from _typeshed import NoneType
from rest_framework.views import exception_handler

ERRORS = {
    '400': 'Обязательное поле',
    '401': 'Учетные данные не были предоставлены',
    '403': 'У вас недостаточно прав для выполнения данного действия.',
    '404': 'Страница не найдена',
    '405': 'Недопустимый метод',
    '0': 'Неизвестная ошибка'
}


def custom_exception_handler(exc, context):
    """Кастомный обрабочик ошибок, проверяет ошибку на наличие в словаре,
    если есть - отдает необходимый ответ, если нет использует стандартный"""
    response = exception_handler(exc, context)
    try:
        status_code = str(response.status_code)
    except AttributeError:
        return response
    if status_code in ERRORS.keys():
        response.data['detail'] = ERRORS[status_code]
    else:
        response.data['detail'] = 'Случайная ошибка'
    return response
