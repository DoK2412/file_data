from typing import Any

response = {
    1: 'Успешное выполнение запроса ',
    2: 'Авторизация не пройдена',
    3: 'Ошибка определения параметров',
    4: 'Отсутствует необходимый параметр',
    5: 'Срок жизни сессии истек',
    6: 'Ошибка микросервиса',
    7: 'Нет доступа к микросерпису',
    8: 'Какая то хуйня проихошла, вообще хз',
    9: 'Срок жизни кода подтверждения истек',
    10: 'Ошибка на стороне сервера',
    11: 'Такое имя папки уже есть.'

}


class ResponseCode():
    def __init__(self, code, data=None):
        self.answercode: int = code
        self.answer: str = response[code]

class ResponseCodeData():
    def __init__(self, code, data=None):
        self.answercode: int = code
        self.answer: str = response[code]
        self.data: Any = data