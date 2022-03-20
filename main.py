from telegram import *
from telegram.ext import * 
from requests import *
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

dispatcher = updater.dispatcher

button_one_text = "Bottom button 1"
button_two_text = "Bottom button 2"

randomPImageUrl = "https://picsum.photos/1200"

allowedUsernames = []

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(button_one_text)], [KeyboardButton(button_two_text)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))

def helpCommand(update: Update, context: CallbackContext):
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help command\n placeholder", )

def textDMCommand(update: Update, context: CallbackContext):
    print(update)
    context.bot.send_message(chat_id=update.message.from_user.id, text="Here is my message in users", )

def getinfoCommand(update: Update, context: CallbackContext):
    print(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{update.message}', )

def messageHandler(update: Update, context: CallbackContext):
    # white list of users
    # if update.effective_chat.username not in allowedUsernames:
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
    #     return
    if button_two_text in update.message.text:
        image = get(randomPImageUrl).content
    if button_one_text in update.message.text:
        image = get(randomPImageUrl).content

    if image:
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="caption")])

        buttons = [
            [InlineKeyboardButton("callback1_text", callback_data="callback1")], 
            [InlineKeyboardButton("callback2_text", callback_data="callback2")]
        ]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="response placeholder")

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    if "callback1" in query:
        logging.info('callback1')
        context.bot.send_message(chat_id=update.effective_chat.id, text='callback1 message')
    
    if "callback2" in query:
        logging.info('callback2')
        context.bot.send_message(chat_id=update.effective_chat.id, text='callback2 message')



# commands
dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("text_dm", textDMCommand))
dispatcher.add_handler(CommandHandler("get_info", getinfoCommand))


dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()