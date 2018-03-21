#!/usr/bin/env python
import os
import random
from typing import Optional

import telebot
from telebot.types import Message, InlineQueryResultArticle, InputTextMessageContent

TOKEN = os.environ['OWL_BOT_TOKEN']
RUS = 'rus'
ENG = 'eng'
GER = 'ger'


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
		'hoot': random.choice(['Ja', 'Ja-Ja', 'Jo', 'Schtimt']),
		'shit': 'Dingsda'
	}
}

thumb_url = f'https://api.telegram.org/file/bot{TOKEN}/photos/file_2.jpg'
bot = telebot.TeleBot(TOKEN)


def get_confirm_message(lang: str):
	if lang not in CONFIRMS:
		lang = RUS
	r = random.random()
	key = 'confirm' if r > 0.5 else 'hoot' if r > 0.1 else 'shit'
	return CONFIRMS[lang][key]


def reply(text: str, message_id: int) -> Optional[dict]:
	if 'филин' in text and 'подтверди' in text:
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
	if 'подтверди' in text:
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
	if 'сколк' in text:
		return {
			'text': 'Пидарасы',
			'reply_to_message_id': message_id
		}
	r = random.randint(1, 100)
	if r < 10:
		return {
			'text': CONFIRMS[RUS]['hoot']
		}
	return None


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def text_handler(message: Message):
	text = message.text.lower()
	chat_id = message.chat.id
	payload = reply(text, message.message_id)
	if payload:
		bot.send_message(chat_id, **payload)


@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	r = InlineQueryResultArticle('1', 'Подтвердить', InputTextMessageContent('Подтверждаю'), thumb_url=thumb_url)
	bot.answer_inline_query(inline_query.id, results=[r])


bot.polling()
