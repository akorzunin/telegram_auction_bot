from telegram import InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import CallbackContext
import requests


randomPImageUrl = "https://picsum.photos/1200"

def startCommand(update: Update, context: CallbackContext):
    buttons = [
        [KeyboardButton('button_one_text')], 
        [KeyboardButton('button_two_text')]
        ]
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Welcome to my bot!", 
        reply_markup=ReplyKeyboardMarkup(buttons),
    )

def helpCommand(update: Update, context: CallbackContext):
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help command\n placeholder", )

def newmsgCommand(update: Update, context: CallbackContext):
    
    buttons = [
            [InlineKeyboardButton("Принять участие в аукционе", callback_data="callback1")], 
            [InlineKeyboardButton("callback2_text", callback_data="callback2")]
    ]


    context.bot.send_media_group(
            # chat_id=-1001663892384, 
            chat_id=update.effective_chat.id, 
            media=[
                InputMediaPhoto(requests.get(randomPImageUrl).content, caption="caption1"),
                InputMediaPhoto(requests.get(randomPImageUrl).content, caption="caption2"),
                InputMediaPhoto(requests.get(randomPImageUrl).content, caption="caption3"),
                ],
            # reply_markup=InlineKeyboardMarkup(buttons), 
            # text="New message\n placeholder",
    ).append(
        context.bot.send_message(
            # chat_id=-1001663892384, 
            chat_id=update.effective_chat.id, 
            reply_markup=InlineKeyboardMarkup(buttons), 
            text="New message\n placeholder\n "
        )
    )

def textDMCommand(update: Update, context: CallbackContext):
    print(update)
    context.bot.send_message(chat_id=update.message.from_user.id, text="Here is my message in users", )

def getinfoCommand(update: Update, context: CallbackContext):
    # print(context)
    # print(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{update.message}', )
    # context.bot.send_message(chat_id=-1001715164845, text=f'{update.message}', )
    # print(context._chat_id_and_data)