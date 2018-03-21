#!/usr/bin/env python
import os
import random

import telebot
from telebot.types import Message, InlineQueryResultArticle, InputTextMessageContent

TOKEN = os.environ['OWL_BOT_TOKEN']
thumb_url = f'https://api.telegram.org/file/bot{TOKEN}/photos/file_2.jpg'
bot = telebot.TeleBot(TOKEN)
# print(bot.get_me())


def get_confirm_message():
	r = random.random()
	return 'Подтверждаю' if r > 0.5 else 'Угу'


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def text_handler(message: Message):
	# print(f"{message.from_user} - {message.text}")
	text = message.text.lower()
	chat_id = message.chat.id
	if 'филин' in text and 'подтверди' in text:
		bot.send_message(chat_id, get_confirm_message(), reply_to_message_id=message.message_id)
	elif 'подтверди' in text:
		bot.send_message(chat_id, get_confirm_message())
	elif 'сколк' in text:
		bot.send_message(chat_id, 'Пидарасы', reply_to_message_id=message.message_id)
	else:
		r = random.randint(1, 100)
		if r < 10:
			bot.send_message(chat_id, 'Угу')


@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	# print(inline_query)
	r = InlineQueryResultArticle('1', 'Подтвердить', InputTextMessageContent('Подтверждаю'), thumb_url=thumb_url)
	bot.answer_inline_query(inline_query.id, results=[r])


bot.polling()
