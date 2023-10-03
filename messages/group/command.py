import logging
from typing import List

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from telegram.helpers import mention_html

import config
from util import reply_html, delete, MSG_REMOVAL_PERIOD, CHAT_ID, MSG_ID


def get_rules() -> List[str]:
    return [
        "1️⃣ Keine Beleidigung anderer Mitglieder.",
        "2️⃣ Kein Spam (mehr als drei einzelne Nachrichten oder Alben hintereinander weitergeleitet).",
        "3️⃣ Keine pornografischen Inhalte.",
        "4️⃣ Keine Aufnahmen von Leichen oder Schwerverletzen.",
        "5️⃣ Keine privaten Inhalte anderer Personen teilen."
    ]


async def send_rules(update: Update, context: CallbackContext):
    await reply_html(update, context, "rules", "\n\n".join(get_rules()))


async def send_loss(update: Update, context: CallbackContext):
    await reply_html(update, context, "loss")


async def send_maps(update: Update, context: CallbackContext):
    await reply_html(update, context, "maps")


async def send_short(update: Update, context: CallbackContext):
    await reply_html(update, context, "short")


async def send_stats(update: Update, context: CallbackContext):
    await reply_html(update, context, "stats")


async def unwarn_user(update: Update, context: CallbackContext):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    if update.message.from_user.id in config.ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in config.ADMINS:
        logging.info(f"unwarning {update.message.reply_to_message.from_user.id} !!")

        context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = []

        await update.message.reply_to_message.reply_text(
            f"Dem Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} wurde alle Verwarnungen erlassen.")


async def warn_user(update: Update, context: CallbackContext):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    if update.message.from_user.id in config.ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in config.ADMINS:
        logging.info(f"warning {update.message.reply_to_message.from_user.id} !!")

        if "users" not in context.bot_data or update.message.reply_to_message.from_user.id not in context.bot_data[
            "users"] or "warn" not in context.bot_data["users"][update.message.reply_to_message.from_user.id]:
            context.bot_data["users"] = {
                update.message.reply_to_message.from_user.id: {"warn": [update.message.reply_to_message.id]}}

        else:
            if update.message.reply_to_message.id in \
                    context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]:
                msg = await update.message.reply_to_message.reply_text(
                    "Der Nutzer wurde für diese Nachricht bereits verwarnt.")
                context.job_queue.run_once(delete, MSG_REMOVAL_PERIOD,
                                           {CHAT_ID: msg.chat_id, MSG_ID: msg.message_id})
                return

            context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"].append(
                update.message.reply_to_message.id)

        warn_amount = len(context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"])

        if warn_amount > 3:
            try:
                logging.info(f"banning {update.message.reply_to_message.from_user.id} !!")
                await context.bot.ban_chat_member(update.message.reply_to_message.chat_id,
                                                  update.message.reply_to_message.from_user.id, until_date=1)
            except TelegramError as e:
                logging.info(f"needs admin: {e}")
                pass

            await update.message.reply_to_message.reply_text(
                f"Aufgrund wiederholter Verstöße habe ich {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} gebannt.")
            return
        else:

            warn_text = f"Der Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} hat die Warnung {warn_amount} von 3 erhalten."
            if len(context.args) != 0:
                if context.args[0].isnumeric():
                    warn_text = f"{warn_text}\n\nGrund: {get_rules()[int(context.args[0]) - 1]}"
                else:

                    warn_text = f"{warn_text}\n\nGrund: {' '.join(context.args)}"
            else:
                warn_text = (
                    f"Hey {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)}‼️ Das musste jetzt echt nicht sein. Bitte verhalte dich besser!"
                    f"\n\n{warn_text}"
                    f"\n\n<i>Mit /rules bekommst du eine Übersicht der Regeln dieser Gruppe.</i>")

            await update.message.reply_to_message.reply_text(warn_text)
