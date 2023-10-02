import logging

from telegram import Update, BotCommandScopeChat
from telegram.error import BadRequest, TelegramError
from telegram.ext import CallbackContext
from telegram.helpers import mention_html

import config
from util import reply_html


async def setup(update: Update, context: CallbackContext):
    general_commands = [
        ("maps", "Karten"),
        ("loss", "Verluste"),
        ("stats", "Statistiken"),
        ("short", "Abkürzungen"),
        ("support", "Unterstützung der Ukrainer"),
        ("channels", "Ukrainekrieg auf Telegram"),
        ("peace", "Russlands Kriege"),
        ("donbass.html", "Beschuss des Donbass seit 2014"),
        ("genozid", "Kein Genozid im Donbass")
    ]
    await context.bot.set_my_commands(general_commands)

    admin_commands = general_commands + [
        ("add_source", "Quelle hinzufügen"),
        ("edit_source", "Quelle bearbeiten"),
        ("add_pattern", "Zu entfernenden Footer hinzufügen"),
        ("warn", "Nutzer verwarnen"),
        ("unwarn", "Verwarnung zurückziehen"),
    ]
    for chat_id in config.ADMINS:
        try:
            await context.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=chat_id))
        except BadRequest:  # to ignore chat not found
            pass

    await update.message.reply_text("Commands updated.")


async def send_rules(update: Update, context: CallbackContext):
    await reply_html(update, context, "rules")


async def unwarn_user(update: Update, context: CallbackContext):
    try:
        await update.message.delete()
    except TelegramError as e:
        logging.info(f"needs admin: {e}")
        pass

    if update.message.from_user.id in config.ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in config.ADMINS:
        logging.info(f"unwarning {update.message.reply_to_message.from_user.id} !!")
        if "users" not in context.bot_data or update.message.reply_to_message.from_user.id not in context.bot_data[
            "users"] or "warn" not in context.bot_data["users"][update.message.reply_to_message.from_user.id]:
            warnings = 0
            context.bot_data["users"] = {update.message.reply_to_message.from_user.id: {"warn": warnings}}

        else:
            warnings = context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]

            if warnings != 0:
                warnings = warnings - 1

            context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = warnings

            await update.message.reply_to_message.reply_text(
                f"Dem Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} wurde eine Warnung erlassen, womit er nur noch {warnings} von 3 hat.")


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
            warnings = 1
            context.bot_data["users"] = {update.message.reply_to_message.from_user.id: {"warn": warnings}}

        else:
            warnings = context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]
            if warnings == 3:
                logging.info(f"banning {update.message.reply_to_message.from_user.id} !!")
                await context.bot.ban_chat_member(update.message.reply_to_message.chat_id,
                                                  update.message.reply_to_message.from_user.id, until_date=1)
                await update.message.reply_to_message.reply_text(
                    f"Aufgrund wiederholter Verstöße habe ich {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} gebannt.")
                return
            else:
                warnings = warnings + 1
                context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = warnings

        warn_text = f"Der Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} hat die Warnung {warnings} von 3 erhalten."
        if len(context.args) != 0:
            warn_text = f"{warn_text}\n\nGrund: {' '.join(context.args)}"
        else:
            warn_text = f"Hey! Das musste jetzt echt nicht sein. Bitte verhalte dich besser!\n\n{warn_text}"

        await update.message.reply_to_message.reply_text(warn_text)



