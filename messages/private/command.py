from telegram import Update, BotCommandScopeChatAdministrators, BotCommandScopeChat
from telegram.error import BadRequest
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

    private_admin_commands = general_commands + [
        ("blacklist", "Gefilterte Begriffe"),
    ]

    for chat_id in config.ADMINS:
        try:
            await context.bot.set_my_commands(private_admin_commands, scope=BotCommandScopeChat(chat_id=chat_id))
        except BadRequest:  # to ignore chat not found
            pass

    await update.message.reply_text("Commands updated.")


async def show_blacklist(update: Update, context: CallbackContext):
    filtered = "\n\n- ".join(config.BLACKLIST)
    await update.message.reply_text(f'Ich lösche folgende Begriffe in der Gruppe:\n\n- {filtered}')
