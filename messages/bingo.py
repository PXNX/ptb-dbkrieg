import datetime
import logging
import random
import re
from typing import List, Union, Dict

import cairosvg
import numpy
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext
from telegram.helpers import mention_html


load_dotenv()

ENTRIES = {
    "Israel": None,
    "Baerbock verurteilt": None,
    "Lauterbach warnt": None,
    "China": None,
    "wirkungsvoll": None,
    "Biden": None,
    "Schwurbler": None,
    "Schneelensky": None,
    "Booster": None,
    "Zwang": None,
    "Drogen": None,
    "geimpft": None,
    "böse_NATO": None,
    "Wunderwaffe": None,
    "Gamechanger": None,
    "Offensive": None,
    "SDF/YPG": None,
    "Hartz_IV": None,
    "Atomkrieg": None,
    "kampferprobt": None,
    "Spinner": None,
    "Weltmacht": None,
    "Kokain": None,
    "HIMARS": None,
    "Krim": None,
    "Russland_droht": None,
    "Biolabor": None,
    "Schlangeninsel": None,
    "Faschist": None,
    "Britischer Geheimdienst": r"Britische(r*) Geheimdienst",
    "Asow": r"A(s|z)o(w|v)",
    "Alina Lipp": r"Alina|Lipp",
    "Erdogan": None,
    "Korruption": None,
    "Konvention": None,
    "Lufthoheit": None,
    "Taiwan": None,
    "Frontverlauf": None,
    "Kinzhal": None,
    "Meinung": None,
    "Lukashenko": r"Lukas(c*)henko",
    "Impfung": r"Impfung|impfen|geimpft",
    "Reichsbürger": None,
    "Trump": None,
    "Schwarzmarkt": None,
    "Troll": None,
    "WEF": None,
    "Klaus Schwab": None,
    "Bill Gates": None,
    "Dimension": None,
    "Reptiloid": None,
    "Gerücht": None,
    "System": None,
    "einsatzbereit": None,
    "Putin_macht bald_ernst": None,
    "Militärexperte": None,
    "Zweiter Weltkrieg": r"Zweite(r|n) Weltkrieg|WW2|WK",
    "Palästina": None,
    "Verluste": None,
    "Logistik": None,
    "Stalingrad": None,
    "Barbarossa": None,
    "Wehrmacht": None,
    "Unfall": None,
    "Raucher": None,
    "Ivan": None,
    "Osterweiterung": None,
    "Vorstoß": None,
    "T-14 Armata": r"T(-*)14|Armata",
    "Kämpf_doch selbst": None,
    "Propaganda": None,
    "Taliban": None,
    "Wahrheit": None,
    "Aber_die_USA": None,
    "Ukraine beschießt Zivilisten": None,
    "Munitionsdepot": None,
    "Selenski fordert": None,
    "Man_muss verhandeln": None,
    "Gas": None,
    "Bayraktar TB2": r"Bayraktar|Baykar|TB2|TB-2",
    "Quelle?": None,
    "Hostomel": None,
    "Elite": None,
    "8_Jahre": None,
    "seit_2014": None,
    "Irpin": None,
    "Butscha": r"But(s*)cha",
    "Massengrab": None,
    "Isjum": None,
    "Goyda": None,
    "Klitschko": None,
    "Chornobayivka": None,
    "Belgorod": None,
    "kapitulieren": None,
    "aufgeben": None,
    "Vakuumbombe": None,
    "thermobarisch": None,
    "Sanktion": None,
    "Deflation": None,
    "Wagner": None,
    "Volksrepublik": None,
    "Referendum": None,
    "russophob": None,
    "Eskalation": None,
    "AKW": r"AKW|Atomkraftwerk",
    "Gaspreis": None,
    "reagiert": None,
    "Globohomo": None,
    "Doppelmoral": None,
    "Euromaidan": None,
    "Clown": None,
    "9/11": None,
    "Rothschild": None,
    "Beischlafbettler": None
}

field_size = 5


def generate_bingo_field():
    key_list = list(ENTRIES)

    random.shuffle(key_list)

    d2 = {}

    for key in key_list:
        #   logging.info(key, ENTRIES[key])
        d2[key] = ENTRIES[key]

    outer = list()

    for x in range(1, field_size * field_size, field_size):
        inner = list()
        #   logging.info(x)

        for entry in list(d2.items())[x:x + field_size]:
            #     logging.info("ENTRY >>>>>>>>> ", entry, entry[0])
            if entry[1] is None:
                regex = entry[0]
            else:
                regex = entry[1]

            inner.append({
                "text": entry[0],
                "checked": False,
                "regex": regex
            })

        outer.append(inner)

    #  logging.info(outer)
    return outer


def check_win(fields: List[List[Dict[str, Union[str, bool]]]]):
    # horizontal condition
    for row in fields:
        if all(item["checked"] for item in row):
            return True

    # vertical condition
    for column in zip(*fields):
        if all(item["checked"] for item in column):
            return True

    return False


def set_checked(text: str, fields: List[List[Dict[str, Union[str, bool]]]]):
    found = list()
    #  logging.info(list(numpy.array(fields).flat))
    for item in list(numpy.array(fields).flat):
        matches = re.findall(item["regex"], text.replace(" ", ""), re.IGNORECASE)
        #   logging.info(item["regex"], text, ">>>", matches)
        if not item["checked"] and len(matches) != 0:
            item["checked"] = True
            found.append(item["text"])
            logging.info(f"{text} is a valid bingo entry")

    return found


def create_svg(field: List[List[Dict[str, Union[str, bool]]]]):
    all_width = 2460
    all_height = 1460

    canvas_width = 2360
    canvas_height = 1200
    border_distance = int((all_width - canvas_width) / 2)
    #  logging.info("border_distance", border_distance)

    svg = f"""<?xml version='1.0' encoding='UTF-8' standalone='no'?>
    <svg
       width='{all_width}'
       height='{all_height}'
       viewBox='0 0 {all_width} {all_height}'
       version='1.1'
       xmlns='http://www.w3.org/2000/svg'
       xmlns:svg='http://www.w3.org/2000/svg'>

    <text y="{border_distance + 60}" x="50%" font-size="60px" font-family="Arial" dominant-baseline="middle"  fill="white" ><tspan dy="0" x="50%" font-weight="bold" text-anchor="middle">Donbass-Bingo</tspan></text>
    """

    line_width = 2
    line_half = int(line_width / 2)
    height_treshold = int((canvas_height - (field_size * line_width)) / field_size + line_width)
    width_treshold = int((canvas_width - (
            field_size * line_width)) / field_size + line_width)
    current_width = 0

    svg_field = f"""
    <svg width="{canvas_width}" height="{canvas_height}"  x="{border_distance - line_half}" y="170"    viewBox='{-line_half} {-line_half} {canvas_width + line_half} {canvas_height + line_half}'>
    """

    curr_x = 0

    while current_width < canvas_width:
        #  logging.info(current_width)

        x_var = f"<svg width=\"{width_treshold}\" height=\"{height_treshold}\"  x=\"{current_width}\""
        current_height = 0
        curr_y = 0

        while current_height < canvas_height:
            #  logging.info(current_height)

            curr_field = field[curr_x][curr_y]
            # logging.info(curr_field)

            textss = curr_field["text"].split(" ")
            for index, value in enumerate(textss):
                textss[index] = value.replace("_", " ")

            inner_text = """<text  font-size="48px" font-family="Arial" dominant-baseline="central" """

            if curr_field["checked"]:
                inner_text += "fill=\"#DC143C\" "
            else:
                inner_text += "fill=\"white\" "

            if len(textss) == 1:
                inner_text += f""" y="50%"><tspan x="50%" text-anchor="middle">{textss[0]}</tspan>"""
            elif len(textss) == 2:
                inner_text += f""" y="40%" ><tspan x="50%" text-anchor="middle" dy="1em">{textss[1]}</tspan><tspan  x="50%" text-anchor="middle" dy="-1em">{textss[0]}</tspan>"""
            elif len(textss) == 3:
                inner_text += f"""y="50%"><tspan x="50%" text-anchor="middle">{textss[1]}</tspan><tspan x="50%" text-anchor="middle" dy="1em">{textss[2]}</tspan><tspan  x="50%" text-anchor="middle" dy="-2em">{textss[0]}</tspan>"""
            else:
                inner_text = "> TOO LONG"

            svg_field += f"""
            {x_var} y="{current_height}" text-align="center">
           <rect x="0" y="0" width="100%" height="100%" stroke="#00BFFF" stroke-width="6px" paint-order="fill" fill="#00004d" />
           {inner_text}</text>
         </svg>
    """
            curr_y += 1
            current_height += height_treshold
        curr_x += 1
        current_width += width_treshold

    logging.info("lines done, now text -----------------")

    svg_field += "</svg>"

    svg += svg_field

    svg += f"""
    <text y="{all_height - border_distance}" x="{all_width - border_distance}" font-size="26px" font-family="Arial" dominant-baseline="middle"  text-anchor="end" fill="gray" >zuletzt aktualisiert {datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}</text>
    </svg>"""

    # logging.info(svg)

    cairosvg.svg2png(bytestring=svg, write_to='field.png', background_color="#000000")


async def handle_bingo(update: Update, context: CallbackContext):
    logging.info(f"bingo check !! {update}")

    text = update.message.text.lower()

    # elif datetime.datetime.now().weekday() == 5 or datetime.datetime.now().weekday() == 6:
    logging.info("checking bingo...")
    if "bingo" not in context.bot_data:
        context.bot_data["bingo"] = generate_bingo_field()
        create_svg(context.bot_data["bingo"])

    found = set_checked(text, context.bot_data["bingo"])
    found_amount = len(found)

    if found_amount != 0:

        if check_win(context.bot_data["bingo"]):
            create_svg(context.bot_data["bingo"])
            with open("field.png", "rb") as f:
                msg = await  update.message.reply_photo(photo=f,
                                                        caption=f"<b>BINGO! 🥳</b>"
                                                                f"\n\n{mention_html(update.message.from_user.id, update.message.from_user.first_name)} hat den letzten Begriff beigetragen. Die erratenen Begriffe sind gelb eingefärbt."
                                                                f"\n\nEine neue Runde beginnt..."
                                                          )
                #todo: add footer
                await msg.pin()
            context.bot_data["bingo"] = generate_bingo_field()
        else:

            text = '<b>Treffer! 🥳</b>\n\n'

            for index, word in enumerate(found):
                text += f'\"{word}\"'

                if index == found_amount - 1:
                    if found_amount == 1:
                        text += " ist ein gesuchter Begriff"
                    else:
                        text += " sind gesuchte Begriffe"

                    text += " im Donbass-Bingo."

                elif index == found_amount - 2:
                    text += " und "

                else:
                    text += ", "

            await update.message.reply_text(text)


async def bingo_field(update: Update, context: CallbackContext):
    try:
        if "bingo" not in context.bot_data:
            context.bot_data["bingo"] = generate_bingo_field()
        create_svg(context.bot_data["bingo"])
        with open("field.png", "rb") as f:
            await update.message.reply_photo(photo=f,
                                             caption=f"<b>Donbass-Bingo</b>\n\n"
                                                     f"Wenn eine in diesem Chat gesendete Nachricht auf dem Spielfeld vorkommendende Begriffe enthält, werden diese rausgestrichen.\n\n"
                                                     f"Ist eine gesamte Zeile oder Spalte durchgestrichen, dann heißt es <b>BINGO!</b> und eine neue Runde startet.\n"
                                                     )
            #todo: add footer
    except FileNotFoundError as e:
        logging.info("No field yet")


async def reset_bingo(update: Update, context: CallbackContext):
    context.bot_data["bingo"] = generate_bingo_field()
    await update.message.reply_text(f"Bingo was reset!\n\n{context.bot_data['bingo']}")
