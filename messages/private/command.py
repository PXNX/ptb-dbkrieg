from telegram import Update, BotCommandScopeChatAdministrators
from telegram.ext import CallbackContext

import config


async def setup(update: Update, context: CallbackContext):
    general_commands = [
        ("rules", "Gruppenregeln"),
        ("maps", "Karten"),
        ("loss", "Verluste"),
        ("stats", "Statistiken"),
        ("short", "Abkürzungen"),
    ]
    await context.bot.set_my_commands(general_commands)

    admin_commands = general_commands + [
        ("warn", "Nutzer verwarnen"),
        ("unwarn", "Verwarnungen erlassen"),
    ]

    await context.bot.set_my_commands(admin_commands, scope=BotCommandScopeChatAdministrators(chat_id=config.GROUP))

    await update.message.reply_text("Commands updated.")
