# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from tgbot.utils.misc.bot_models import UserDB, FSM, RS
from tgbot.services.api_sqlite import get_wallets, update_wallets, new_ballance_user, write_new_wallets
from tgbot.keyboards.z_all_inline import check_deposit_keyboard, my_wallet, deposit_keyboard
from tgbot.utils.create_wallet import create_wallet, check_payments, get_last_tx
from tgbot.utils.send_token import send_tokens
import asyncio

from tgbot.utils.token_to_dollar import tokenn_in_dollars, get_dollars_in_rub

router_deposit = Router()
import tgbot.config as cfg


@router_deposit.callback_query(F.data == 'wallet')
async def wallet_handler(call: CallbackQuery, bot: Bot, state: FSM, rSession: RS, user: UserDB):
    await state.clear()
    text = f"<b>Ваш ID:  <code>{user.user_id} </code>\n" \
           f"Баланс: <code>{user.ballance:.2f} </code>{cfg.CURRENCY} </b>\n"
    await call.message.edit_text(text, reply_markup=my_wallet)


@router_deposit.callback_query(F.data == 'deposit')
async def deposit_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("<b>👆 Пополнить</b>\n\n"
                                 "📋 Выберите нужную криптовалюту для пополнения баланса:",
                                 reply_markup=deposit_keyboard())
    await call.answer()


@router_deposit.callback_query(F.data.startswith('deposit;'))
async def make_deposit_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    token = call.data.split(';')[1]
    print(token)
    if token == "USDT_TRC20":
        snd_min = f"<b>👆 Пополнить {token}</b>\n\nПереведите на этот адрес нужную вам сумму, но<b> не менее 20 USDT</b>. ‼️Если вы отправили сумму меньше, бот не зачислит ваши средства. Отправьте недостающую до 20 USDT сумму. После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n "
    else:
        convert = "" if "USD" in token else "<b>При пополнении токены будут конвертированны в USDT</b>\n\n"
        snd_min = f"<b>👆 Пополнить {token}</b>\n\nПереведите на этот адрес нужную вам сумму После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n {convert}"

    wal = get_wallets(user_id=call.from_user.id)
    if token == "USDT_BEP20":
        token = "BUSD"
    elif token == "TRX":
        token = "USDT_TRC20"
    if wal is not None:
        adress = wal[f'address_{token.lower()}']
    else:
        update_wallets(user_id=call.from_user.id)
        adress = None

    if adress is None or len(adress) == 0:
        adress, key = await create_wallet(token)
        arg_adress, arg_key = f'address_{token.lower()}', f'primary_key_{token.lower()}'
        kwargs = {arg_adress: adress, arg_key: key}
        write_new_wallets(user_id=call.from_user.id, **kwargs)

    # if token == "BUSD":
    #     snd_min = "Переведите на этот адрес нужную вам сумму После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n "
    # # elif:
    # #     snd_min = "Переведите на этот адрес нужную вам сумму После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n "
    # else:
    #     snd_min = "Переведите на этот адрес нужную вам сумму, но<b> не менее 20 USDT</b>. ‼️Если вы отправили сумму меньше, бот не зачислит ваши средства. Отправьте недостающую до 20 USDT сумму. После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n "

    await call.message.edit_text(f"{snd_min}"
                                 f"<code>{adress}</code>",
                                 reply_markup=await check_deposit_keyboard(call.data.split(';')[1]))
    await call.answer()


@router_deposit.callback_query(F.data == 'wallet')
async def wallet(call: CallbackQuery, state: FSMContext, user: UserDB):
    await state.clear()
    text = f"<b>Ваш ID:</b>  <code>{user.user_id} </code>\n" \
           f"<b>Баланс:</b>  <code>{user.ballance:.2f} </code><b>USDT</b> \n"
    await call.message.edit_text(text, reply_markup=my_wallet)


@router_deposit.callback_query(F.data.startswith('address;'))
async def address_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    token = call.data.split(';')[1]
    if token == "BUSD":
        token = "USDT_BEP20"
    elif token == "TRX":
        token = "USDT_TRC20"
    
    adress = get_wallets(user_id=call.from_user.id)[f'address_{token.lower()}']
    await call.message.answer(adress)
    await call.answer()


@router_deposit.callback_query(F.data.startswith('check_payment;'))
async def check_payment(call: CallbackQuery, state: FSMContext, bot: Bot, user: UserDB):
    await state.clear()
    token = call.data.split(';')[1]
    print(token)
    wallet = get_wallets(user_id=call.from_user.id)
    if token == "USDT_BEP20":
        tok = "busd"
    elif token == "TRX":
        tok = "usdt_trc20"
    else:
        tok = token.lower()
    adres, key = wallet[f'address_{tok}'], wallet[f'primary_key_{tok}']

    balance = await check_payments(token, adres, )

    await call.message.delete()
    await get_last_tx(adres)
    if token == "BUSD" and balance > 0 or token == "USDT_BEP20" and balance > 0 or token == "USDT_TRC20" and balance >= 20 or token == "TRX" and balance >= 1:

        tx = await send_tokens(from_address=adres,
                               from_private_key=key,
                               to_address=None, amount=balance,
                               token=token,
                               deposit=True
                               )

        if tx is not None and len(tx) == 2 and tx[0] == 'error':
            await call.message.answer(f"<b>👆 Пополнить {token}</b>\n\n"
                                      "⚠ Мы видим вашу транзакцию, но к сожалению не можем её подтвердить. Обратитесь "
                                      "в "
                                      "поддержку.\n\n "
                                      "Переведите на этот адрес нужную вам сумму. После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n"
                                      f"<code>{adres}</code>",
                                      )
            try:
                await bot.send_message(cfg.ADMINS[0], f"ошибка отправки {token} на основной адресс \n\n"
                                                      f"Пользователь {call.message.chat.username}\n"
                                                      f"Cумма {balance} {token} "
                                                      f"\n Адрес {adres}\n"
                                                      f"Ключ {key} \n "
                                                      f"Ошибка  {tx[1]}")
            except:
                pass
            return
        if token == "TRX":
            balance = await tokenn_in_dollars(token, balance)
        balance = await get_dollars_in_rub(balance)
        new_ballance_user(user_id=user.user_id, amout=float(balance))
        await call.message.answer(f"💰 Ваш счёт пополнен на {balance} {cfg.CURRENCY}")
    else:
        if token == "USDT_TRC20":
            snd_min = "Переведите на этот адрес нужную вам сумму, но<b> не менее 20 USDT</b>. ‼️Если вы отправили сумму меньше, бот не зачислит ваши средства. Отправьте недостающую до 20 USDT сумму. После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n "
        else:
            convert = "" if "USD" in token else "<b>При пополнении токены будут конвертированны в USDT</b>\n\n"
            snd_min = f"Переведите на этот адрес нужную вам сумму После перевода, нажмите на кнопку «🔃 Проверить платеж»\n\n {convert} "
        await call.message.answer(f"<b>👆 Пополнить {token}</b>\n\n"
                                  "⚠ Транзакция ещё не найдена. Попробуйте позже.\n\n"
                                  f"{snd_min} "
                                  f"<code>{adres}</code>", reply_markup=await check_deposit_keyboard(token))
    if token == "BUSD" or token == "USDT_BEP20":
        try:
            await asyncio.sleep(15)
            await send_tokens(from_address=adres,
                              from_private_key=key,
                              to_address=None,
                              amount=0,
                              token="BNB",
                              deposit=True
                              )

        except:
            pass
    # await call.answer()
