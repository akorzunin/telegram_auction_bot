# from telegram import *
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, CommandHandler, Updater
# from telegram import 
#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
# read TOKEN from .env
TOKEN = os.getenv('TOKEN')
updater = Updater(token=TOKEN)

import logging
DEBUG = __debug__ 
LOG_FILE_NAME = 'auction_bot.log'
format = '%(asctime)s [%(levelname)s]: %(message)s'
logger = logging.basicConfig(
    filename=LOG_FILE_NAME if not DEBUG else None, 
    format=format,
    encoding='utf-8', 
    level=logging.INFO, 
)
if not DEBUG:
    logging.getLogger(logger).addHandler(logging.StreamHandler())

from modules.bot_commands import *
from modules.bot_handlers import *


dispatcher = updater.dispatcher

# commands
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("text_dm", textDMCommand))
dispatcher.add_handler(CommandHandler("get_info", getinfoCommand))
dispatcher.add_handler(CommandHandler("new_msg", newmsgCommand))


dispatcher.add_handler(MessageHandler(Filters.is_automatic_forward, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()