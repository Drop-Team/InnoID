from aiogram import types
from aiogram.types.message import ParseMode

from bot.command_tools.message_handlers import add_message_handler
from bot.tools.users import get_user


@add_message_handler(commands=["authorize"])
async def authorize_command(msg: types.message.Message):
    user = get_user(msg.from_user.id)
    if user.is_authorized:
        answer = "🔑 You already authorized in InnoID as {}.".format(user.email)
        await msg.answer(answer, parse_mode=ParseMode.HTML)
    else:
        answer = f"🔑 Follow the link below to login."
        await msg.answer(answer, parse_mode=ParseMode.HTML, reply_markup=user.get_telegram_keyboard_markup())
