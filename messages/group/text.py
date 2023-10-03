import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.helpers import mention_html

import config


async def filter_text(update: Update, context: CallbackContext):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass


async def admin(update: Update, context: CallbackContext):
    logging.info(f"admin: {update.message}")

    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    if update.message.reply_to_message is not None:
        response = ""
        for a in config.ADMINS:
            response += mention_html(a, "​")

        if update.message.reply_to_message.is_automatic_forward:
            response += "Danke für deine Meldung, wir Admins prüfen das 😊"
        else:
            response += "‼️ Ein Nutzer hat deine Nachricht gemeldet. Wir Admins prüfen das."

        await update.message.reply_to_message.reply_text(response)
