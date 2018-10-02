#!/usr/bin/env python
import os
import random
from typing import Optional

import telebot
from telebot.types import Message, InlineQueryResultArticle, InputTextMessageContent

from texts import ORIGINAL_JOKE

TOKEN = os.environ['OWL_BOT_TOKEN']
RUS = 'rus'
ENG = 'eng'
GER = 'ger'
GEO = 'geo'  # Georgia


CONFIRMS = {
    RUS: {
        'confirm': 'Подтверждаю',
        'hoot': 'Угу',
        'shit': 'Хуйня'
    },
    ENG: {
        'confirm': 'Confirm',
        'hoot': 'Yea',
        'shit': 'Bullshit'
    },
    GER: {
        'confirm': 'Bekräftige',
        'hoot': random.choice(['Ja', 'Ja-Ja', 'Jo', 'Stimmt']),
        'shit': 'Dingsda'
    },
    GEO: {
        'confirm': 'ვადასტურებ',
        'hoot': 'ჰო',
        'shit': 'ამაზრზენი'
    }
}

OWL_NAMES = {
    'филин': RUS,
    'owl': ENG,
    'der uhu': GER,
    'ზარნაშო': GEO
}
AGREE_NAMES = {
    'подтверди': RUS,
    'подтверждаешь': RUS,
    'confirm': ENG,
    'bekräftig': GER,
    'დადასტურება': GEO
}
THUMB_URL = f'https://api.telegram.org/file/bot{TOKEN}/photos/file_2.jpg'
STIKER_ID = 'CAADAgADTQQAAqYWEAABbWQv8i-T5yIC'
bot = telebot.TeleBot(TOKEN)


def get_confirm_message(lang: str):
    if lang not in CONFIRMS:
        lang = RUS
    r = random.random()
    key = 'confirm' if r > 0.5 else 'hoot' if r > 0.1 else 'shit'
    return CONFIRMS[lang][key]


def detect_language(text: str) -> Optional[str]:
    language = None
    for name in AGREE_NAMES.keys():
        if name in text:
            language = AGREE_NAMES[name]
    return language


def check_is_reply_needed(text: str) -> bool:
    is_reply_needed = False
    for owl_name in OWL_NAMES.keys():
        if owl_name in text:
            is_reply_needed = True
    return is_reply_needed


def get_reply_payload(text: str, message_id: int) -> dict:
    reply_data = {}
    language = detect_language(text)
    is_reply_needed = check_is_reply_needed(text)
    r = random.randint(1, 100)

    if language:
        if language == RUS:
            if r < 5:
                reply_data['sticker'] = True

        reply_data['text'] = get_confirm_message(language)
        if is_reply_needed:
            reply_data['reply_to_message_id'] = message_id
    else:
        if r < 10:
            reply_data['text'] = CONFIRMS[RUS]['hoot']

    return reply_data


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, text=ORIGINAL_JOKE)


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def text_handler(message: Message):
    text = message.text.lower()
    chat_id = message.chat.id
    payload = get_reply_payload(text, message.message_id)

    if 'sticker' in payload:
        bot.send_sticker(chat_id, STIKER_ID)
    elif payload:
        bot.send_message(chat_id, **payload)


@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
    r = InlineQueryResultArticle('1', 'Подтвердить', InputTextMessageContent('Подтверждаю'), thumb_url=THUMB_URL)
    bot.answer_inline_query(inline_query.id, results=[r])


bot.polling(timeout=60)
