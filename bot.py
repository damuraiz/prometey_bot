import logging

import os
import json

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

from service import PrometeyService

service = PrometeyService()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    user = service.get_user(update.effective_user.id)
    if not user:
        logger.info(f"User with telegram_id = {update.effective_user.id} not found. Registering..")
        service.register_user(update.effective_user.id)
        user = service.get_user(update.effective_user.id)
        logger.info(f"User with telegram_id = {user.telegram_user_id} registered. Id: {user.id}")

    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Ну что давай, собирать видосики")

def create(update, context):
    user = service.get_user(update.effective_user.id)
    if len(context.args) == 0 or not user:
        pass
    else:
        name = context.args[0]
        content = service.create_content(user.id, name)
        text = f'Контент ID:{content.id} c именем <b>{content.name}</b> - создан и установлен по умолчанию!'
        logger.info(text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML)

def my(update, context):
    user = service.get_user(update.effective_user.id)
    logger.info(user.contents)
    text = ''
    if user.current_content:
        text += f"Текущий контент ID:<b>{user.current_content.id}</b> - <b>{user.current_content.name}</b>\n\n"
    for content in sorted(user.contents, key = lambda content: content.id, reverse=True):
        text += f"<b>{content.id}</b> - {content.name} - {content.status}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML)

def change(update, context):
    user = service.get_user(update.effective_user.id)
    service.change_current(user.id, int(context.args[0]))
    #todo проверка на права
    content = user.current_content
    text = f'Контент ID:{content.id} c именем <b>{content.name}</b> - установлен по умолчанию!'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML)

def finish(update, context):
    user = service.get_user(update.effective_user.id)
    #todo проверка на права
    content = service.finish_video(user.id)

    text = f'Контент id:{content.id} - <b>{content.name}</b> - переведен в статус {content.status}'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML)

def info(update, context):
    user = service.get_user(update.effective_user.id)
    content = user.current_content
    text = f'id: {content.id}:<b>{content.name}</b>\nВсего: {content.total_video_count},' \
           f' скачано: {content.downloaded_video_count}, длительность: {content.total_duration}'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML)


def add_url(update, context):
    url = update.message.text
    user = service.get_user(update.effective_user.id)
    video = service.add_url(user.id, url)
    if video:
        text = f"Ссылка {video.url} добавлена! id:{video.id}" #todo убрать id
    else:
        text = "Что-то пошло не так"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def error_callback(update, context):

    #todo пока не работает
    try:
        raise context.error
    except TelegramError as err:
        logger.error(err)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Что-то пошло не так!',
            parse_mode=ParseMode.HTML)



def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    with open(os.path.join('cfg', 'config.json')) as f:
        config = json.load(f)

    updater = Updater(token=config['bot_token'], use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('create', create))
    updater.dispatcher.add_handler(CommandHandler('my', my))
    updater.dispatcher.add_handler(CommandHandler('change', change))
    updater.dispatcher.add_handler(CommandHandler('finish', finish))
    updater.dispatcher.add_handler(CommandHandler('info', info))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, add_url))

    updater.dispatcher.add_error_handler(error_callback)


    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()