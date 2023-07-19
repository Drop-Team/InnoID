from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import Config
import aiohttp


async def create_connection(code: int, telegram_id: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f"{Config.API_URL}/v2/admin/user_id/code",
                json={
                    "code": code,
                },
        ) as response:
            data = await response.json()
            print(data)
            user_id = data.get("user_id", None)

        async with session.post(
                url=f"{Config.API_URL}/v2/admin/connections/telegram",
                json={
                    "user_id": user_id,
                    "telegram_id": telegram_id,
                },
        ) as response:
            data = await response.json()
            print(data)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await create_connection(code=context.args[0], telegram_id=str(update.message.chat.id))
    await update.message.reply_text(
        text="Well done!",
    )


app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))

app.run_polling()
