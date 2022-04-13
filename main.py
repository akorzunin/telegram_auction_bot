
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update


from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, CommandHandler, Updater
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from modules.err_handler import error_handler
from modules.bot_handlers import queryHandler
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

from modules import bot_commands
from modules import bot_handlers
from modules.conversation_handlers import conv_handler
from modules.post_upload_conversation import post_upload_conversation

dispatcher = updater.dispatcher

# old commands
dispatcher.add_handler(CommandHandler("start", bot_commands.startCommand))
dispatcher.add_handler(CommandHandler("help", bot_commands.helpCommand))
dispatcher.add_handler(CommandHandler("text_dm", bot_commands.textDMCommand))
dispatcher.add_handler(CommandHandler("get_info", bot_commands.getinfoCommand))
dispatcher.add_handler(CommandHandler("new_msg", bot_commands.newmsgCommand))
dispatcher.add_handler(CommandHandler("get_image", bot_commands.get_image_Command))

# new commands
dispatcher.add_handler(CommandHandler("post_from_id", bot_commands.post_from_id))


# dispatcher.add_handler(MessageHandler(Filters.is_automatic_forward, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(bot_handlers.queryHandler))

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(post_upload_conversation)
dispatcher.add_error_handler(error_handler)

updater.start_polling()