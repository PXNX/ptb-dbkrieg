import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext

_MSG_REMOVAL_PERIOD = 1200
_CHAT_ID = "chat_id"
_MSG_ID = "msg_id"


async def delete(context: CallbackContext):
    await context.bot.delete_message(context.job.data[_CHAT_ID], context.job.data[_MSG_ID])


async def reply_html(update: Update, context: CallbackContext, file_name: str):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    try:
        with open(f"res/de/{file_name}.html", "r", encoding='utf-8') as f:
            text = f.read()

        if update.message.reply_to_message is not None:
            msg = await update.message.reply_to_message.reply_text(text)
        else:
            msg = await context.bot.send_message(update.message.chat_id, text)

        context.job_queue.run_once(delete, _MSG_REMOVAL_PERIOD, {_CHAT_ID: msg.chat_id, _MSG_ID: msg.message_id})

    except Exception as e:
        logging.error(f"Couldn't read html-file {file_name}: {e}")
        pass
