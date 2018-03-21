#!/usr/bin/env python
import os

import telebot
from telebot.types import Message

TOKEN = os.environ['OWL_BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def text_handler(message: Message):
	text = message.text.lower()
	chat_id = message.chat.id
	if 'филин' in text and 'подтверди' in text:
		bot.send_message(chat_id, 'Подтверждаю', reply_to_message_id=message.message_id)
	elif 'подтверди' in text:
		bot.send_message(chat_id, 'Подтверждаю')


bot.polling()
