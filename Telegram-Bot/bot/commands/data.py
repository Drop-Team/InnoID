from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ParseMode

from bot.command_tools.callback_query import add_callback_query
from bot.command_tools.message_handlers import add_message_handler
from bot.tools.api_requests import ApiDelete
from bot.tools.users import get_user

forget_me_confirm_callback_data = "forgetme_confirm_user_"
forget_me_deny_callback_data = "forgetme_deny_user_"


@add_message_handler(commands=["data"])
async def data_command(msg: types.message.Message):
    user = get_user(msg.from_user.id)

    if not user.is_authorized:
        return await msg.answer("😕 You are not logged in, so we do not store your data.")

    answer = f"The data we store:\n\nEmail: {user.email}"
    return await msg.answer(answer, parse_mode=ParseMode.HTML)


@add_message_handler(commands=["forgetme"])
async def forget_me_command(msg: types.message.Message):
    user = get_user(msg.from_user.id)

    if not user.is_authorized:
        return await msg.answer("You are not logged in, so there is no need to delete your data.")

    answer = f"Are you sure you want to delete all your data from InnoID?\n\n" \
             f"All applications using InnoID will no longer be able to request your data " \
             f"and confirm your student status."
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton("Yes, I want to delete all my data",
                                      callback_data=forget_me_confirm_callback_data + str(user.id))
    no_button = InlineKeyboardButton("No, I will save my account",
                                     callback_data=forget_me_deny_callback_data + str(user.id))
    keyboard.add(yes_button)
    keyboard.add(no_button)
    return await msg.answer(answer, parse_mode=ParseMode.HTML, reply_markup=keyboard)


@add_callback_query(lambda cb: cb.data.startswith(forget_me_confirm_callback_data))
async def forget_me_confirm_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer("You are not authorized.")

    response = ApiDelete.make_request("users", user.telegram_id)
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")

    answer = "💔 All your data has been successfully deleted.\n\nWe will be glad to see you again."
    await callback_query.message.edit_text(answer)


@add_callback_query(lambda cb: cb.data.startswith(forget_me_deny_callback_data))
async def forget_me_deny_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer("You are not authorized.")

    await callback_query.message.edit_text("❤ Thank you for staying with us!")
