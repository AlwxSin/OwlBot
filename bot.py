#!/usr/bin/env python
import os
import random

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
        'shit': 'ვადასტურებ'  # for now same as confirm
    }
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


def get_reply_payload(text: str, message_id: int) -> dict:
    r = random.randint(1, 100)

    if 'филин' in text and 'подтверди' in text:
        if r < 5:
            return {'sticker': True}
        return {
            'text': get_confirm_message(RUS),
            'reply_to_message_id': message_id
        }
    if 'owl' in text and 'confirm' in text:
        return {
            'text': get_confirm_message(ENG),
            'reply_to_message_id': message_id
        }
    if 'der uhu' in text and 'bekräftig' in text:
        return {
            'text': get_confirm_message(GER),
            'reply_to_message_id': message_id
        }
    if 'ზარნაშო' in text and 'დადასტურება' in text:
        return {
            'text': get_confirm_message(GEO),
            'reply_to_message_id': message_id
        }
    if 'подтверди' in text:
        if r < 5:
            return {'sticker': True}
        return {
            'text': get_confirm_message(RUS),
        }
    if 'confirm' in text:
        return {
            'text': get_confirm_message(ENG),
        }
    if 'bekräftig' in text:
        return {
            'text': get_confirm_message(GER),
        }
    if 'დადასტურება' in text:
        return {
            'text': get_confirm_message(GER),
        }

    if r < 10:
        return {
            'text': CONFIRMS[RUS]['hoot']
        }
    return {}


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
