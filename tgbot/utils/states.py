from aiogram.fsm.state import StatesGroup, State


class NewBallance(StatesGroup):
    user_id = State()
    amout = State()

class Sender(StatesGroup):
    text = State()
    photo = State()
    button = State()
    url = State()

class SearchUser(StatesGroup):
    user_id = State()


class SearchNameStandart(StatesGroup):
    lastname = State()
    firstname = State()
    middlename = State()
    day = State()
    mounth = State()
    year = State()


class SearchNameFull(StatesGroup):
    lastname = State()
    firstname = State()
    middlename = State()
    birthday = State()


class SearchPhone(StatesGroup):
    number = State()

class SearchPassport(StatesGroup):
    number = State()

class SearchINN(StatesGroup):
    number = State()

class SearchEmail(StatesGroup):
    address = State()

class SearchSnils(StatesGroup):
    number = State()

class SearchAvto(StatesGroup):
    number = State()

class SearchVin(StatesGroup):
    number = State()

class SearchINN_U(StatesGroup):
    number = State()

class SearchScoring(StatesGroup):
    lastname = State()
    firstname = State()
    middlename = State()
    birthday = State()

class SearchCredit(StatesGroup):
    lastname = State()
    firstname = State()
    middlename = State()
    birthday = State()

class StorageQiwi(StatesGroup):
    here_input_qiwi_secret = State()
    here_input_qiwi_login = State()
    here_input_qiwi_token = State()
    here_input_qiwi_amount = State()

class NewFaq(StatesGroup):
    button = State()
    description = State()

class EditFaq(StatesGroup):
    description = State()
    button = State()

class Withdraw(StatesGroup):
    token = State()
    max_amount = State()
    amount = State()
    adress = State()

class ListenMessageForward(StatesGroup):
    message = State()

class Linepay(StatesGroup):
    sum = State()