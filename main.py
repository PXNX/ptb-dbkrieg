import logging
import os
import re
from datetime import datetime

from telegram.constants import ParseMode
from telegram.ext import Defaults, ApplicationBuilder, filters, CommandHandler, PicklePersistence, MessageHandler, \
    CallbackQueryHandler

import config
from config import TOKEN
from messages.command import send_rules, setup, unwarn_user, warn_user
from messages.private.captcha import send_captcha, click_captcha, unclick_captcha
from messages.text import admin, filter_text

_LOG_FILENAME = rf"./logs/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H-%M-%S')}.log"
os.makedirs(os.path.dirname(_LOG_FILENAME), exist_ok=True)
logging.basicConfig(
    format="%(asctime)s %(levelname)-5s %(funcName)-20s [%(filename)s:%(lineno)d]: %(message)s",
    encoding="utf-8",
    filename=_LOG_FILENAME,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    app = (ApplicationBuilder().token(TOKEN)
           .defaults(Defaults(parse_mode=ParseMode.HTML, disable_web_page_preview=True))
           .persistence(PicklePersistence(filepath="persistence"))
           .build())

    group = filters.Chat(config.GROUP)

    app.add_handler(CommandHandler("warn", warn_user, group))
    app.add_handler(CommandHandler("unwarn", unwarn_user, group))
    app.add_handler(CommandHandler("rules", send_rules))
    app.add_handler(CommandHandler("setup", setup, filters.Chat(config.ADMINS)))
    app.add_handler(CommandHandler("captcha", send_captcha))

    app.add_handler(CallbackQueryHandler(click_captcha,r"captcha_.+_.+", ))
 #   app.add_handler(CallbackQueryHandler(unclick_captcha, r"captcha_.+_True", ))

    app.add_handler(MessageHandler(group & filters.Regex("^@admin"), admin))
    app.add_handler(MessageHandler(
        group & filters.TEXT & filters.Regex(re.compile("|".join(config.BLACKLIST), re.IGNORECASE)),
        filter_text))

    print("### RUN LOCAL ###")
    app.run_polling(poll_interval=1)
