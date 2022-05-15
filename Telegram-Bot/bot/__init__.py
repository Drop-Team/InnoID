import asyncio
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bot.command_tools.callback_query import register_callback_queries
from bot.command_tools.message_handlers import register_message_handlers
from bot.commands import info, authorization, data, apps
from bot.logger import logger
from bot.loops import event
from bot.metrics import Metrics

bot = Bot(token=os.getenv("INNOID_TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)


async def on_startup(dp):
    bot_info = await bot.get_me()
    print(f"Logged in as {bot_info.full_name} ({bot_info.mention})")
    Metrics.start_time.set_to_current_time()


def start():
    register_message_handlers(dp)
    register_callback_queries(dp)

    loop = asyncio.get_event_loop()
    loop.create_task(event.check_for_event(bot, 1))

    print("Starting bot...")
    executor.start_polling(dp, on_startup=on_startup)
