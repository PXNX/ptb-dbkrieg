import random
from random import randint

from PIL import Image, ImageDraw, ImageFont
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import config
from util import MSG_REMOVAL_PERIOD

supported_emojis = ['🃏', '🎤', '🎥', '🎨', '🎩', '🎬', '🎭', '🎮', '🎯', '🎱', '🎲', '🎷', '🎸', '🎹', '🎾', '🏀', '🏆', '🏈', '🏉',
                    '🏐',
                    '🏓', '💠', '💡', '💣', '💨', '💸', '💻', '💾', '💿', '📈', '📉', '📊', '📌', '📍', '📎', '📏', '📐', '📞', '📟',
                    '📠',
                    '📡', '📢', '📣', '📦', '📹', '📺', '📻', '📼', '📽', '🖥', '🖨', '🖲', '🗂', '🗃', '🗄', '🗜', '🗝', '🗡', '🚧',
                    '🚨',
                    '🛒', '🛠', '🛢', '🧀', '🌭', '🌮', '🌯', '🌺', '🌻', '🌼', '🌽', '🌾', '🌿', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏',
                    '🍚',
                    '🍛', '🍜', '🍝', '🍞', '🍟', '🍪', '🍫', '🍬', '🍭', '🍮', '🍯', '🍺', '🍻', '🍼', '🍽', '🍾', '🍿', '🎊', '🎋',
                    '🎍',
                    '🎏', '🎚', '🎛', '🎞', '🐌', '🐍', '🐎', '🐚', '🐛', '🐝', '🐞', '🐟', '🐬', '🐭', '🐮', '🐯', '🐻', '🐼', '🐿',
                    '👛',
                    '👜', '👝', '👞', '👟', '💊', '💋', '💍', '💎', '🔋', '🔌', '🔪', '🔫', '🔬', '🔭', '🔮', '🕯', '🖊', '🖋', '🖌',
                    '🖍',
                    '🥚', '🥛', '🥜', '🥝', '🥞', '🦊', '🦋', '🦌', '🦍', '🦎', '🦏', '🌀', '🌂', '🌑', '🌕', '🌡', '🌤', '⛅️', '🌦',
                    '🌧',
                    '🌨', '🌩', '🌰', '🌱', '🌲', '🌳', '🌴', '🌵', '🌶', '🌷', '🌸', '🌹', '🍀', '🍁', '🍂', '🍃', '🍄', '🍅', '🍆',
                    '🍇',
                    '🍈', '🍉', '🍐', '🍑', '🍒', '🍓', '🍔', '🍕', '🍖', '🍗', '🍘', '🍙', '🍠', '🍡', '🍢', '🍣', '🍤', '🍥', '🍦',
                    '🍧',
                    '🍨', '🍩', '🍰', '🍱', '🍲', '🍴', '🍵', '🍶', '🍷', '🍸', '🍹', '🎀', '🎁', '🎂', '🎃', '🎄', '🎈', '🎉', '🎒',
                    '🎓',
                    '🎙', '🐀', '🐁', '🐂', '🐃', '🐄', '🐅', '🐆', '🐇', '🐕', '🐉', '🐓', '🐖', '🐗', '🐘', '🐙', '🐠', '🐡', '🐢',
                    '🐣',
                    '🐤', '🐥', '🐦', '🐧', '🐨', '🐩', '🐰', '🐱', '🐴', '🐵', '🐶', '🐷', '🐸', '🐹', '👑', '👒', '👠',
                    '👡', '👢', '💄', '💈', '🔗', '🔥', '🔦', '🔧', '🔨', '🔩', '🔰', '🔱', '🕰', '🕶', '🕹', '🖇', '🚀', '🤖', '🥀',
                    '🥁',
                    '🥂', '🥃', '🥐', '🥑', '🥒', '🥓', '🥔', '🥕', '🥖', '🥗', '🥘', '🥙', '🦀', '🦁', '🦂', '🦃', '🦄', '🦅', '🦆',
                    '🦇',
                    '🦈', '🦉', '🦐', '🦑', '⭐️', '⏰', '⏲', '⚠️', '⚡️', '⚰️', '⚽️', '⚾️', '⛄️', '⛅️', '⛈', '⛏', '⛓',
                    '⌚️',
                    '☎️', '⚜️', '✏️', '⌨️', '☁️', '☃️', '☄️', '☕️', '☘️', '☠️', '♨️', '⚒', '⚔️', '⚙️', '✈️', '✉️',
                    '✒️']


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def generate_captcha(user_id: int):
    background = Image.open(f'res/img/bg_{randint(1, 4)}.jpg', )
    paste_image_list = list()
    emoji_names = list()

    random.shuffle(supported_emojis)

    for i in range(4):
        emoji_names.append(supported_emojis[i])
        paste_image_list.append(supported_emojis[i])

    width = int(background.width / 3)
    heigth = int(background.height / 2)

    position = [(width * 1 - 274 * 1, heigth * 1 - 274 * 1), (int(width * 3.4 - 274 * 3), heigth * 1 - 274 * 1),
                (width * 1 - 274 * 1, heigth * 2 - 274 * 2), (width * 2 - 274 * 2, int(heigth * 2.2 - 274 * 2))]
    print(position)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(r"AppleColorEmoji.ttf", 137)

    for i, emoji in enumerate(paste_image_list):
        text_layer = Image.new('RGBA', (274, 274), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_layer)
        draw.text(xy=(0, 0), text=emoji, fill=(255, 255, 255), embedded_color=True, font=font)

        rotated_text_layer = text_layer.rotate(random.randint(0, 350),
                                               expand=True, fillcolor=(0, 0, 0, 0), resample=Image.BICUBIC)
        background.paste(rotated_text_layer, position[i], rotated_text_layer)

    emoji_captcha_path = f"captcha_{user_id}.png"

    background.save(emoji_captcha_path, "PNG", quality=100)
    res = emoji_names, emoji_captcha_path

    print(res)
    return res


async def decline(context: CallbackContext):
    await context.bot.decline_chat_join_request(config.GROUP, int(context.job.data))


async def send_captcha(update: Update, context: CallbackContext):
    answer, captcha = generate_captcha(update.chat_join_request.from_user.id)
    random.shuffle(supported_emojis)

    options = list(answer)
    for em in supported_emojis:
        if len(options) == 12:
            break
        if em not in options:
            options.append(em)
    random.shuffle(options)

    keyboard = []
    for row in chunks(options, 4):
        row_btns = []

        for btn in row:
            row_btns.append(InlineKeyboardButton(btn, callback_data=f"captcha_{btn}_{False}"))

        keyboard.append(row_btns)

    print(keyboard)

    context.user_data["captcha"] = answer
    print(answer)

    await context.bot.send_photo(update.chat_join_request.from_user.id, open(captcha, "rb"),
                                 "Bitte löse das Captcha! Klicke dazu alle im Bild befindlichen Emojis an",
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    context.job_queue.run_once(decline, MSG_REMOVAL_PERIOD, update.callback_query.from_user.id)


async def click_captcha(update: Update, context: CallbackContext):
    btn = update.callback_query.data.split("_")[1]

    keynard = list(map(list, update.callback_query.message.reply_markup.inline_keyboard))
    options = []
    selected_count = 0
    for x, btrow in enumerate(keynard):
        for y, btne in enumerate(btrow):
            #     print(btne.callback_data.split("_")[2])

            if btne.callback_data.split("_")[1] == btn:
                if btne.callback_data.split("_")[2] == "False":
                    keynard[x][y] = InlineKeyboardButton("✅", callback_data=f"captcha_{btn}_True")
                    print("SET TRUE")
                    options.append(btne.callback_data.split("_")[1])
                    selected_count += 1
                else:
                    keynard[x][y] = InlineKeyboardButton(btn, callback_data=f"captcha_{btn}_False")

            if btne.callback_data.split("_")[2] == "True":
                options.append(btne.callback_data.split("_")[1])
                selected_count += 1
                print("selc", selected_count)

    answer_count = 0
    for em in options:
        print(em, context.user_data["captcha"])
        if em in context.user_data["captcha"]:
            answer_count += 1

    print(options, answer_count, selected_count)
    if answer_count == 4 and selected_count == 4:
        await update.callback_query.message.delete()
        await context.bot.send_message(update.callback_query.from_user.id,
                                       "Vielen Dank für das Lösen des Captchas 😊"
                                       "\n\nBitte warte kurz. Die Admins überprüfen dein Profil.")


    else:
        await update.callback_query.edit_message_reply_markup(InlineKeyboardMarkup(keynard))
        await update.callback_query.answer()
