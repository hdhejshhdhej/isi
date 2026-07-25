from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.utils.const_functions import ikb


def create_faq(all_faq):
    kb = InlineKeyboardBuilder()
    for i in all_faq:
        check_box = "✅ " if i['is_show'] else ""
        kb.add(ikb(text=check_box+i['name_button'], data=f"edit_faq;{i['id']}"))
    kb.add(ikb(text="Cоздать", data='create_faq'))
    kb.adjust(1)
    return kb.as_markup()

def edit_faq(line,is_show):
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Изменить описание RU", data=f"description_faq;ru;{line}"))
    # kb.add(ikb(text="Изменить описание EN", data=f"description_faq;en;{line}"))
    kb.add(ikb(text="Изменить название кнопки RU", data=f"button_faq;ru;{line}"))
    # kb.add(ikb(text="Изменить название кнопки  EN", data=f"button_faq;en;{line}"))
    if is_show:
        kb.add(ikb(text="Не показывать", data=f'faq_is_show;0;{line}'))
    else:
        kb.add(ikb(text="Паказать", data=f'faq_is_show;1;{line}'))
    kb.add(ikb(text="Удалить", data=f"del_faq;{line}"))
    kb.add(ikb(text="Назад", data="back_faq"))
    kb.adjust(1)
    return kb.as_markup()

def see_faq_user(all_faq):
    kb = InlineKeyboardBuilder()
    for i in all_faq:
        kb.add(ikb(text=i['name_button'], data=f"see_faq;{i['id']}"))
    # kb.add(ikb(text="Назад", data="info"))
    kb.adjust(1)
    return kb.as_markup()


def back_faq_info():
    kb = InlineKeyboardBuilder()
    kb.add(ikb(text="Назад", data="faq_info"))
    kb.adjust(1)
    return kb.as_markup()


