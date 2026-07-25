# - *- coding: utf- 8 - *-
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb


def sender_button(name, url):
    return InlineKeyboardBuilder().row(ikb(name, url=url)).as_markup()


# Тестовые админ инлайн кнопки


def search_main():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🧍 Поиск по ФИО", data='choose_search_people'))
    kb.add(ikb(text=" 📞Проверка номера", data='choose_phone'))
    kb.add(ikb(text="🪪 Поиск по паспорту", data='choose_passport'))
    kb.add(ikb(text="📄 Поиск по ИНН", data='choose_inn_fl'))
    kb.add(ikb(text="📧 Проверка  по E-mail", data='choose_email'))
    kb.add(ikb(text="📋 Поиск  по СНИЛС", data='choose_snils'))
    kb.add(ikb(text="🚘 Поиск  по авто", data='choose_avto'))
    kb.add(ikb(text="🚘 Поиск  по VIN", data='choose_vin'))
    kb.add(ikb(text="💼 Поиск  по ИНН ЮЛ", data='choose_inn'))
    kb.add(ikb(text="🧍 Скоринг ФЛ ", data='choose_scoring'))
    kb.add(ikb(text="🧍 Кредитный рейтинг ", data='choose_credit'))
    kb.adjust(2)
    return kb.as_markup()


def choose_search_people_kb():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Начать поиск 👤", data='name_standart'))
    #kb.add(ikb(text="Расширенный поиск 👥", data='name_full'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def back_search():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def not_money():
    kb = InlineKeyboardBuilder()
    kb.add(ikb("⬇️Пополнить баланс", data='deposit'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_search_people_kb_back():
    kb = InlineKeyboardBuilder()
    kb.add(ikb("⬇️Пополнить баланс", data='deposit'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_search_people_kb_standart():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_people_standart'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_phone():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_phone'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose__passport():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_passport'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_inn_fl():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_inn_fl'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_inn():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_inn'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_snils():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_snils'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_avto():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_avto'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_vin():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_vin'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_email_kb():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_email'))
    kb.add(ikb(text="Назад", data='back_search'))
    kb.adjust(1)
    return kb.as_markup()


def choose_search_name_full():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_name_full'))
    kb.add(ikb(text="Назад", data='choose_search_people'))
    kb.adjust(1)
    return kb.as_markup()


def choose_search_scoring():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_scoring'))
    kb.add(ikb(text="Назад", data='choose_search_people'))
    kb.adjust(1)
    return kb.as_markup()
#Кредитный рейтинг
def choose_search_credit():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="🔍 Начать поиск", data='start_search_credit'))
    kb.add(ikb(text="Назад", data='choose_search_people'))
    kb.adjust(1)
    return kb.as_markup()


my_wallet = InlineKeyboardBuilder(
).row(
    ikb("⬇️Пополнить", data='deposit'),
    # ikb("⬆️ Вывести", data="withdraw"),
).as_markup()


async def check_deposit_keyboard(token):
    return InlineKeyboardBuilder(
    ).row(
        ikb("📄 Адрес отдельно", data=f"address;{token}"),
    ).row(
        ikb("🔃 Проверить платеж", data=f"check_payment;{token}"),
    ).row(
        ikb("⬅ Назад", data="deposit")).as_markup()


def deposit_keyboard():
    keyboard = InlineKeyboardBuilder()
    # keyboard.add(ikb("LinePay Visa/MasterCard/Мир/BTC/Qiwi и др.", data="linepay_deposit"))
    keyboard.add(ikb(text="USDT TRC20", data='deposit;USDT_TRC20'))
    keyboard.add(ikb(text="USDT BEP 20", data='deposit;USDT_BEP20'))
    keyboard.add(ikb(text="TRX", data='deposit;TRX'))
    keyboard.add(ikb(text="⬅ Назад", data='wallet'))
    keyboard.adjust(1, 2, 1)
    return keyboard.as_markup()


back_withdraw_keyboard = InlineKeyboardBuilder(
).row(
    ikb("⬅ Назад", data="wallet"),
).as_markup()


def pay_linepay(url):
    return InlineKeyboardBuilder(
).row(
    ikb("Оплатить", url=url),
).as_markup()

async def back_amount_withdraw_keyboard():
    return InlineKeyboardBuilder(
    ).row(
        ikb("⬅ Назад", data=f'withdraw'),
    ).as_markup()


def withdraw_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(ikb(text="USDT TRC20", data='withdraw;USDT_TRC20'))
    keyboard.add(ikb(text="USDT BEP 20", data='withdraw;USDT_BEP20'))
    keyboard.add(ikb(text="⬅ Назад", data='wallet'))
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def feed_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(ikb(text="💬Ответить", data='feed_back'))
    keyboard.adjust(1)
    return keyboard.as_markup()


def info_link(all_faq):
    kb = InlineKeyboardBuilder()

    kb.add(ikb("💬 Поддержка", data="feed_back"))
    if all_faq:
        kb.add(ikb("FAQ", data="faq_info"))
    kb.adjust(1, 1)
    return kb.as_markup()


def my_history():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text=" Проверка ФИО Стандартный поиск 👤", data='history;name_standart'))
    #kb.add(ikb(text=" Проверка ФИО Раcширеный поиск 👥", data='history;name_full'))
    kb.add(ikb(text=" 📞Проверка номера", data='history;phone'))
    kb.add(ikb(text="🪪 Поиск по паспорту", data='history;passport'))
    kb.add(ikb(text="📄 Поиск по ИНН", data='history;inn_fl'))
    kb.add(ikb(text="📧 Проверка  по E-mail", data='history;email'))
    kb.add(ikb(text="📋 Поиск  по СНИЛС", data='history;snils'))
    kb.add(ikb(text="🚘 Поиск  по авто", data='history;avto'))
    kb.add(ikb(text="🚘 Поиск  по VIN", data='history;vin'))
    kb.add(ikb(text="💼 Поиск  по ИНН", data='history;inn'))
    kb.add(ikb(text="🧍 Скоринг ФЛ ", data='history;scoring'))
    kb.add(ikb(text="🧍 Кредитный рейтинг ", data='history;credit'))
    kb.adjust(1, 1, 2)
    return kb.as_markup()


def pag_history(total_index, cnt_all, id, type_request):
    kb = InlineKeyboardBuilder()
    if cnt_all > 1:
        kb.add(ikb(text="<", data=f'prew;{type_request};{total_index}'))
        kb.add(ikb(text="Скачать", data=f'download;{id}'))
        kb.add(ikb(text=">", data=f'next;{type_request};{total_index}'))
        kb.add(ikb(text="⬅ Назад", data='back_history'))
        kb.adjust(3, 1)
    else:
        kb.add(ikb(text="Скачать", data=f'download;{id}'))
        kb.add(ikb(text="⬅ Назад", data='back_history'))
        kb.adjust(1, 1)
    return kb.as_markup()


def update_qiwi_balancce(link):
    kb = InlineKeyboardBuilder()

    kb.add(ikb(text="Cсылка для оплаты", url=link))
    kb.add(ikb(text='↩️', data=f'deposit'))
    kb.adjust(1, 1)
    return kb.as_markup()

def first_name_name_standart():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Пропустить", data="nxt_state_name"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()


def name_name_name_standart():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Без Имени", data="nxt_state_otcher"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()

def name_name_standart():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Без Отчества", data="nxt_state"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()

def name_no_day():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Без дня", data="name_no_day"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()


def name_no_month():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Без месяца", data="name_no_month"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()


def name_no_year():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Без года", data="name_no_year"))
    kb.add(ikb(text='Отмена', data=f'close_this'))
    kb.adjust(1, 1)
    return kb.as_markup()