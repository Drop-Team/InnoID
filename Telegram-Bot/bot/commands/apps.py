from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ParseMode

from bot.command_tools.callback_query import add_callback_query
from bot.command_tools.message_handlers import add_message_handler
from bot.tools.api_requests import ApiGet, ApiPost, ApiPut, ApiDelete
from bot.tools.users import get_user

user_states = {}
NOT_AUTHORIZED_MSG = "You are not authorized in InnoID. Use /authorize command."


class UserState:
    def __init__(self, action: str, app_id: int = None):
        self.action = action
        self.app_id = app_id


class KeyboardCallbacks:
    apps_list = "apps_list"
    select_app = "select_app_"
    change_app_name = "change_name_app_"
    get_app_token = "get_token_app_"
    revoke_app_token = "revoke_token_app_"
    delete_app = "delete_app_"
    delete_app_confirm = "delete_confirm_app_"

    @staticmethod
    def get_app_id(cb_data: str, pattern: str) -> int:
        return int(cb_data.split(pattern)[1])

    @staticmethod
    def get_inline_button(text: str, pattern: str, app_id: int = None) -> InlineKeyboardButton:
        callback_data = pattern + str(app_id) if app_id else pattern
        return InlineKeyboardButton(text, callback_data=callback_data)


def get_apps_list(tg_user_id: int) -> (str, InlineKeyboardMarkup):
    user = get_user(tg_user_id)
    if not user.is_authorized:
        return NOT_AUTHORIZED_MSG, None

    apps_response = ApiGet.make_request("apps")
    if apps_response.status_code != 200:
        return "😕 Something went wrong, please try again later.", None

    all_apps = apps_response.json().get("apps", [])
    user_apps = list(filter(lambda app: app["tg_author_id"] == tg_user_id, all_apps))
    if not user_apps:
        return "You have no registered applications.\n" \
               "Register new with /newapp.", None

    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    for app in user_apps:
        button = InlineKeyboardButton(app["name"], callback_data=KeyboardCallbacks.select_app + str(app["id"]))
        keyboard_markup.insert(button)

    return "Choose an app:", keyboard_markup


@add_message_handler(commands=["myapps"])
async def my_apps_command(msg: types.message.Message):
    text, keyboard_markup = get_apps_list(msg.from_user.id)
    await msg.answer(text, reply_markup=keyboard_markup)


@add_message_handler(commands=["newapp"])
async def new_app_command(msg: types.message.Message):
    user = get_user(msg.from_user.id)
    if not user.is_authorized:
        return await msg.answer(NOT_AUTHORIZED_MSG)

    user_states[msg.from_user.id] = UserState("set_new_app_name")
    await msg.answer("Send the name for the new app.")


@add_callback_query(lambda cb: cb.data == KeyboardCallbacks.apps_list)
async def apps_list_cb(callback_query: types.callback_query.CallbackQuery):
    text, keyboard_markup = get_apps_list(callback_query.from_user.id)
    await callback_query.message.edit_text(text, reply_markup=keyboard_markup)


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.select_app))
async def selected_app_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.select_app)

    response = ApiGet.make_request("apps", app_id)
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")

    app_data = response.json()
    text = "Selected app: <b>{}</b>\nWhat do you want to do with it?".format(app_data["name"])

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.row(
        KeyboardCallbacks.get_inline_button("API Token", KeyboardCallbacks.get_app_token, app_id),
        KeyboardCallbacks.get_inline_button("Change name", KeyboardCallbacks.change_app_name, app_id)
    )
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("Delete app", KeyboardCallbacks.delete_app, app_id))
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("<< Back to my apps", KeyboardCallbacks.apps_list))

    await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard_markup)
    await callback_query.answer()


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.get_app_token))
async def get_app_token_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.get_app_token)

    response = ApiGet.make_request("apps", app_id)
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")

    app_data = response.json()

    text = "Token for app <b>{}</b>:\n\n<code>{}</code>".format(app_data["name"], app_data["token"])

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("Revoke Token", KeyboardCallbacks.revoke_app_token, app_id))
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("<< Back to app", KeyboardCallbacks.select_app, app_id))

    await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard_markup)
    await callback_query.answer()


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.revoke_app_token))
async def revoke_app_token_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.revoke_app_token)

    response = ApiPut.make_request("apps", app_id, "reset_token")
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")

    app_data = response.json()["app"]

    text = "Token has been successfully revoked for app <b>{}</b>.\n" \
           "New token:\n\n<code>{}</code>".format(app_data["name"], app_data["token"])

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("<< Back to app", KeyboardCallbacks.select_app, app_id))

    await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard_markup)
    await callback_query.answer()


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.delete_app))
async def delete_app_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.delete_app)

    response = ApiGet.make_request("apps", app_id)
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")

    app_data = response.json()

    text = "Are you sure you want to delete app <b>{}</b>".format(app_data["name"])

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("Yes", KeyboardCallbacks.delete_app_confirm, app_id))
    keyboard_markup.add(KeyboardCallbacks.get_inline_button("<< No, back to app", KeyboardCallbacks.select_app, app_id))

    await callback_query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard_markup)
    await callback_query.answer()


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.delete_app_confirm))
async def delete_app_confirm_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.delete_app_confirm)

    response = ApiDelete.make_request("apps", app_id)
    if response.status_code != 200:
        return await callback_query.answer("Something went wrong.")
    await callback_query.answer("App has been successfully deleted.")

    text, keyboard_markup = get_apps_list(callback_query.from_user.id)
    await callback_query.message.edit_text(text, reply_markup=keyboard_markup)


@add_callback_query(lambda cb: cb.data.startswith(KeyboardCallbacks.change_app_name))
async def change_app_name_cb(callback_query: types.callback_query.CallbackQuery):
    user = get_user(callback_query.from_user.id)
    if not user.is_authorized:
        return await callback_query.answer(NOT_AUTHORIZED_MSG)

    app_id = KeyboardCallbacks.get_app_id(callback_query.data, KeyboardCallbacks.change_app_name)
    user_states[callback_query.from_user.id] = UserState("change_app_name", app_id=app_id)
    await callback_query.message.answer("Send the new name for the app.")
    await callback_query.answer()


@add_message_handler(lambda msg: msg.from_user.id in user_states, is_not_command=True)
async def set_app_name(msg: types.message.Message):
    user = get_user(msg.from_user.id)
    if not user.is_authorized:
        return await msg.answer(NOT_AUTHORIZED_MSG)

    name = msg.text
    if not name or 3 > len(name) or len(name) > 20:
        return await msg.answer("The length of the app name should be from 3 to 20 characters.")

    user_state = user_states.pop(msg.from_user.id)
    action = user_state.action
    app_id = user_state.app_id
    if action == "change_app_name":
        data = {"name": name}
        response = ApiPut.make_request("apps", app_id, json=data)
        if response.status_code != 200:
            return await msg.answer("Something went wrong.")

        keyboard_markup = InlineKeyboardMarkup()
        keyboard_markup.add(KeyboardCallbacks.get_inline_button("<< Back to my apps", KeyboardCallbacks.apps_list))
        await msg.answer("Name of the app has been successfully updated.", reply_markup=keyboard_markup)
    if action == "set_new_app_name":
        data = {"tg_author_id": msg.from_user.id, "name": name}
        response = ApiPost.make_request("apps", json=data)
        if response.status_code != 200:
            return await msg.answer("Something went wrong.")

        answer = "The app has been successfully created. You can check it using /myapps.\n\n" \
                 "Use this token to access API: <code>{}</code>\n\n" \
                 "You can read more about API here:\nhttps://docs.innoid.ru".format(response.json()["app"]["token"])
        await msg.answer(answer, parse_mode=ParseMode.HTML)
