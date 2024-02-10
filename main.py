import logging
import os
import re
from datetime import datetime

from telegram.constants import ParseMode
from telegram.ext import Defaults, ApplicationBuilder, filters, CommandHandler, PicklePersistence, MessageHandler, \
    CallbackQueryHandler, ChatJoinRequestHandler

import config
from config import TOKEN
from messages.bingo import bingo_field, reset_bingo, handle_bingo
from messages.group.command import send_rules, unwarn_user, warn_user, send_maps, send_short, send_stats, send_loss
from messages.group.text import admin, filter_text
from messages.private.captcha import send_captcha, click_captcha
from messages.private.command import setup, show_blacklist

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
    app.add_handler(CommandHandler("loss", send_loss))
    app.add_handler(CommandHandler("maps", send_maps))
    app.add_handler(CommandHandler("short", send_short))
    app.add_handler(CommandHandler("stats", send_stats))
    app.add_handler(CommandHandler("setup", setup, filters.Chat(config.ADMINS)))
    app.add_handler(CommandHandler("blacklist", show_blacklist, filters.Chat(config.ADMINS)))

    app.add_handler(CallbackQueryHandler(click_captcha, r"captcha_.+_.+", ))
    app.add_handler(ChatJoinRequestHandler(callback=send_captcha, chat_id=config.GROUP, block=False))
    #   app.add_handler(CallbackQueryHandler(unclick_captcha, r"captcha_.+_True", ))

    app.add_handler(MessageHandler(group & filters.Regex("^@admin"), admin))
    blacklist = r")|((^|(?!^)\s)".join(config.BLACKLIST)
    blacklist_re = re.compile(fr"((^|(?!^)\s){blacklist})", re.IGNORECASE)

 #   app.add_handler( MessageHandler(group & (filters.Regex(blacklist_re) | filters.CaptionRegex(blacklist_re)),
          #             filter_text))

    app.add_handler(CommandHandler("bingo", bingo_field, filters.User(config.ADMINS)))
    app.add_handler(CommandHandler("reset_bingo", reset_bingo, filters.Chat(config.ADMINS)))
    app.add_handler(MessageHandler(
        filters.UpdateType.MESSAGE & filters.TEXT # & group
        #    & ~filters.User(   config.ADMINS)
        & ~filters.IS_AUTOMATIC_FORWARD & filters.UpdateType.MESSAGE,
        handle_bingo))

    print("### RUN LOCAL ###")
    app.run_polling(poll_interval=1)
