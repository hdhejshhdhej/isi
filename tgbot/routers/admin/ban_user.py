from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.config import ADMINS, CURRENCY
from tgbot.keyboards.admin.ban_user import usr_info
from tgbot.keyboards.admin.main import back_admin_menu, close_this
from tgbot.services.api_sqlite import update_userx, get_userx
from tgbot.utils.misc.bot_models import FSM
from tgbot.utils.states import SearchUser

router_ban = Router()

@router_ban.message(Text(text="Инфо/Бан"))
async def new_ballans(message: Message, state: FSM, ):
    await state.clear()
    await message.answer("Отправьте ID пользователя или user_name", reply_markup=back_admin_menu)
    await state.set_state(SearchUser.user_id)


@router_ban.message(SearchUser.user_id, F.text)
async def new_ballans(message: Message, state: FSM, ):
    usr = get_userx(user_id=message.text)
    if usr is None:
        username = (message.text[1:]).lower() if message.text[0] == "@" else message.text.lower()
        usr = get_userx(user_name=username)

    if usr is not None:
        ban = 'Да' if usr['ban'] else 'Нет'
        txt = f"<b>ID:</b>  <code>{usr['user_id']} </code>\n" \
              f"<b>Имя:</b>  <code>{usr['first_name']} </code>\n" \
              f"<b>Фамилия:</b>  <code>{usr['last_name']} </code>\n" \
              f"<b>Username:</b>  <code>{usr['user_name']} </code>\n" \
              f"<b>Баланс:</b>  <code>{round(float(str(usr['ballance'])), 2)} </code><b>{CURRENCY}</b> \n" \
              f"<b>Блокировка:</b>  <code>{ban} </code>\n"

        key = None if usr['user_id'] in ADMINS else usr_info(usr['ban'], usr['user_id'])
        await state.clear()
        await message.answer(text=txt, reply_markup=key)
    else:
        await message.answer("Некорректный ввод, повторите попытку", reply_markup=close_this)

@router_ban.callback_query(F.data.startswith('blocked_user'))
@router_ban.callback_query(F.data.startswith('unblocked_user'))
async def ban_user(call: CallbackQuery, state: FSM,):
    await state.clear()
    data = call.data.split(';')
    ban =  'Нет'  if data[0] == 'blocked_user' else 'ДА'
    usr = get_userx(user_id=int(data[1]))
    banned = 0  if data[0] == 'blocked_user'else 1
    txt = f"<b>ID:</b>  <code>{usr['user_id']} </code>\n" \
          f"<b>Имя:</b>  <code>{usr['first_name']} </code>\n" \
          f"<b>Фамилия:</b>  <code>{usr['last_name']} </code>\n" \
          f"<b>Username:</b>  <code>{usr['user_name']} </code>\n" \
          f"<b>Баланс:</b>  <code>{round(float(str(usr['ballance'])), 2)} </code><b>{CURRENCY}</b> \n" \
          f"<b>Блокировка:</b>  <code>{ban} </code>\n"
    key = None if int(data[1]) in ADMINS else usr_info(banned, usr['user_id'])
    update_userx(int(data[1]), ban=banned)
    await call.message.edit_text(text=txt, reply_markup=key)