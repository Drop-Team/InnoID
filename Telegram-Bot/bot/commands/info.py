from aiogram import types
from aiogram.types.message import ParseMode

from bot.command_tools.message_handlers import add_message_handler
from bot.tools.users import get_user


@add_message_handler(commands=["start"])
async def start_command(msg: types.message.Message):
    answer = "👋 Welcome to @InnoIDBot, this is a service from @DropTeamDev for authorizing using Telegram aliases.\n\n" \
             "❓ Use /help for more info.\n\n"

    user = get_user(msg.from_user.id)
    if user.is_authorized:
        answer += "🔑 You already authorized in InnoID as {}.".format(user.email)
        await msg.answer(answer, parse_mode=ParseMode.HTML)
    else:
        answer += f"First you need to sign in.\n" \
                  f"🔑 Follow the link below to login."
        await msg.answer(answer, parse_mode=ParseMode.HTML, reply_markup=user.get_telegram_keyboard_markup())


@add_message_handler(commands=["help"])
async def help_command(msg: types.message.Message):
    answer = "InnoID is unified authorization system for Innopolis University students and employees.\n" \
             "It can be used by third-party apps (bots) to identify you are a student.\n\n" \
             "If you want to use InnoID HTTP API, check the documentation: https://docs.innoid.ru\n\n" \
             "/help - Shows this message\n" \
             "/privacy - Get privacy policy\n" \
             "/authorize - Get instruction for authorization\n" \
             "/data - Get all data InnoID saved for your telegram ID\n" \
             "/forgetme - Remove all data InnoID saved for your telegram ID\n" \
             "/newapp - Register an app to access InnoID API\n" \
             "/myapps - Get your registered apps for InnoID API\n\n" \
             "Developers & Support: @DropTeamDev\n\n" \
             "Our products are open source, so you can find InnoID repositories on GitHub:\n" \
             "Telegram Bot: https://github.com/Drop-Team/InnoID-Telegram-Bot\n" \
             "API: https://github.com/Drop-Team/InnoID-API"

    await msg.answer(answer, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@add_message_handler(commands=["privacy"])
async def privacy_command(msg: types.message.Message):
    answer = "Our full public privacy policy: https://bit.ly/2Yu2L4z\n\n" \
             "• We save your email address & Telegram account ID for identification & statistics"

    await msg.answer(answer, parse_mode=ParseMode.HTML)
