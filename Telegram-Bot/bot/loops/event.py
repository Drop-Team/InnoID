import asyncio
import os

import aiohttp
from aiogram import Bot

from bot.metrics import Metrics
from bot.tools.users import get_user, decrypt_telegram_id
from bot.logger import logger


async def process_authorization_code(bot: Bot, code: str, telegram_id: int):
    data = None
    access_token = None
    mail = None
    already_authorized_msg = "You already authorized."
    fail_msg = "😕 Something went wrong, please try again."
    success_msg = "You have successfully logged in as {}.\n\n" \
                  "If you came here from another bot or website, you can now return.\n\n" \
                  "❤ Thank you for using InnoID."

    user = get_user(telegram_id)
    if user.is_authorized:
        return bot.send_message(telegram_id, already_authorized_msg)

    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://login.microsoftonline.com/organizations/oauth2/v2.0/token",
                data={
                    "client_id": os.getenv("INNOID_AZURE_CLIENT_ID"),
                    "redirect_uri": os.getenv("INNOID_REDIRECT_AFTER_LOGIN"),
                    "grant_type": "authorization_code",
                    "client_secret": os.getenv("INNOID_AZURE_CLIENT_SECRET"),
                    "code": code
                }
        ) as response:
            if response.status == 200:
                data = await response.json()
                access_token = data.get("access_token", None)
        if not access_token:
            logger.info(f"Cannot get access token during authorization (response: {response.status}, data: {data})")
            return await bot.send_message(telegram_id, fail_msg)

        async with session.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                mail = data.get("mail", None)

        if not mail:
            logger.info(f"Cannot get mail during authorization (response: {response.status}, data: {data})")
            return await bot.send_message(telegram_id, fail_msg)

    user.is_authorized = True
    user.email = mail

    save_result = user.save()
    if not save_result:
        logger.info(f"Cannot save results during authorization (user: {user.to_dict()} mail: {mail})")
        return await bot.send_message(telegram_id, fail_msg)

    await bot.send_message(telegram_id, success_msg.format(mail))


async def check_for_event(bot: Bot, seconds):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        os.getenv("INNOID_LONGPOLL_GET_EVENT_URL"),
                        headers={"Authorization": "Bearer {}".format(os.getenv("INNOID_LONGPOLL_AUTH_TOKEN"))}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        event = data.get("event", None)
                        if event and event.get("type", None) == "authorization_code":
                            code = event["code"]
                            telegram_id = decrypt_telegram_id(event["encrypted_telegram_id"])
                            if telegram_id.isdigit():
                                await process_authorization_code(bot, code, int(telegram_id))
            Metrics.event_check.labels("success").inc()
        except Exception:
            Metrics.event_check.labels("fail").inc()
        await asyncio.sleep(seconds)
