# - *- coding: utf- 8 - *-
from dataclasses import dataclass
from datetime import datetime

from aiogram.fsm.context import FSMContext

from tgbot.services.api_session import RequestsSession

FSM = FSMContext
RS = RequestsSession


# Упрощённый вызов из словаря
class WrapperMapDict:
    def __init__(self, get_dict: dict):
        self.get_dict = get_dict

    def get_value(self):
        return self.get_dict

    def __getattr__(self, item: str) -> 'WrapperMapDict':
        return self.__class__(self.get_dict.get(item))

    def __repr__(self):
        return repr(self.get_dict)


# Модель пользователя
@dataclass
class UserDB:
    id: int
    user_id: int
    user_name: str
    first_name: str
    last_name: str
    ballance: float
    ban: int
    # lang:str
    user_date: datetime
    message_thread: int
    feed_back: str

