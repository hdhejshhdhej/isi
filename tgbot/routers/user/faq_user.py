from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.admin.faq_inline import see_faq_user, back_faq_info
from tgbot.keyboards.z_all_inline import info_link
from tgbot.services.api_sqlite import get_faq, get_faqs
from tgbot.utils.misc.bot_models import UserDB, FSM
from aiogram import Router, Bot, F


faq_user_router = Router()



@faq_user_router.message(Text(text="ℹ️ Инфо"))
async def faq_menu(message: Message, state: FSM):
    await state.clear()
    all_faq = get_faqs(is_show=True)
    await message.answer('Пожалуйста, выберете интересующий вас вопрос', reply_markup=info_link(all_faq))

@faq_user_router.callback_query(Text(text="faq_info"))
async def faq_menu(call: CallbackQuery, state: FSM):
    await state.clear()
    all_faq = get_faqs(is_show=True)
    await call.message.edit_text('Пожалуйста, выберете интересующий вас вопрос', reply_markup=see_faq_user(all_faq))



@faq_user_router.callback_query(F.data.startswith("see_faq"))
async def faq_menu(call: CallbackQuery, state: FSM):
    await state.clear()
    all_faq = get_faq(id=call.data.split(';')[1])
    await call.message.edit_text(text=all_faq['description'], reply_markup=back_faq_info(),disable_web_page_preview=False)

