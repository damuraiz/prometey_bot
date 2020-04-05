from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext

import os
import json

with open(os.path.join('cfg', 'config.json')) as f:
    config = json.load(f)

updater = Updater(token=config['bot_token'], use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Добавляем видосики")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()