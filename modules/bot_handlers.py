from telegram import InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import CallbackContext
import logging
import requests

randomPImageUrl = "https://picsum.photos/1200"


def messageHandler(update: Update, context: CallbackContext):
    # white list of users
    # if update.effective_chat.username not in allowedUsernames:
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
    #     return
    logging.info('[HANDLER CALL]')
    if 'button_two_text' in update.message.text:
        image = requests.get(randomPImageUrl).content
    if 'button_one_text' in update.message.text:
        image = requests.get(randomPImageUrl).content

    if image:

        buttons = [
            [InlineKeyboardButton("callback1_text", callback_data="callback1")], 
            [InlineKeyboardButton("callback2_text", callback_data="callback2")]
        ]
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="caption")])
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="response placeholder")

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    if "callback1" in query:
        logging.info('callback1')
        print(update)
        context.bot.send_message(chat_id=update.callback_query.from_user.id, text='Вы приняли участие в аукционе')
    
    if "callback2" in query:
        logging.info('callback2')
        context.bot.send_message(chat_id=update.effective_chat.id, text='callback2 message')

    if "new_msg" in query:
        logging.info('new_msg')
        context.bot.send_message(chat_id=update.effective_chat.id, text='new_msg message')