import logging
import re
from typing import Final, Optional

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext

MSG_REMOVAL_PERIOD: Final[int] = 1200
CHAT_ID: Final[str] = "chat_id"
MSG_ID: Final[str] = "msg_id"


async def delete(context: CallbackContext):
    await context.bot.delete_message(context.job.data[CHAT_ID], context.job.data[MSG_ID])


async def reply_html(update: Update, context: CallbackContext, file_name: str, replacement: Optional[str]=None):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    try:
        with open(f"res/de/{file_name}.html", "r", encoding='utf-8') as f:
            text = f.read()

        if "{}" in text:
            text = re.sub(r"{}", replacement, text)

        if update.message.reply_to_message is not None:
            msg = await update.message.reply_to_message.reply_text(text)
        else:
            msg = await context.bot.send_message(update.message.chat_id, text)

        context.job_queue.run_once(delete, MSG_REMOVAL_PERIOD, {CHAT_ID: msg.chat_id, MSG_ID: msg.message_id})

    except Exception as e:
        logging.error(f"Couldn't read html-file {file_name}: {e}")
        pass
