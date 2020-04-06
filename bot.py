from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

def bot1():

    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo, ich bin Hugo. Wie kann ich dir helfen?")

    def echo(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    updater = Updater(token='1063279949:AAGWcbOI5-bhpt2mJdtWFoSGkZIQYzFOzEs', use_context=True)
    dispatcher = updater.dispatcher
    #logs falls was schief läuft
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()