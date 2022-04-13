from msilib.schema import Error
from telegram import InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import CallbackContext
import requests
from modules.post_upload_conversation import send_post_to_channel
from settings.env import DEBUG_CHAT_ID
from settings.env import MAIN_CHANNEL_ID

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
    # implement to post method
def get_image_Command(update: Update, context: CallbackContext):

    context.bot.send_media_group(
            # chat_id=-1001663892384, 
            chat_id=update.effective_chat.id, 
            media=[
                InputMediaPhoto(requests.get(randomPImageUrl).content, caption="New image"),
                ],
    )

def textDMCommand(update: Update, context: CallbackContext):
    print(update)
    context.bot.send_message(chat_id=update.message.from_user.id, text="Here is my message in users", )

def getinfoCommand(update: Update, context: CallbackContext):
    # force use error_handler
    assert 0

### NEW COMMANDS

def post_from_id(update: Update, context: CallbackContext):

    # get item id from message
    try:
        item_id = int(context.args[0])
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Please enter an id after command\n example: /post_from_id 123", 
        )
    except ValueError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Id must be an integer \n example: /post_from_id 123", 
        )


    # read item by id from DB

    headers = {
        'accept': 'application/json',
    }

    params = {
        'id': item_id,
    }

    r = requests.get(
        url='http://192.168.1.125:8000/auc_ext/item_by_id/', 
        headers=headers, 
        params=params,
    )
    if r.status_code != 200:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="DB error", 
        )
        raise ValueError # TODO make custom error
    DB_data = r.json()
    # assert 1
    # fill up context.user_data w/ data from DB
    context.user_data['Title']  = DB_data['title']
    context.user_data['Description'] = DB_data['description']
    context.user_data['Price'] = DB_data['price']

    photo_urls = DB_data['photo'].split('|')
    context.user_data['photos'] = [dict(file=i) for i in photo_urls]

    send_post_to_channel(
        update=update,
        context=context,
        chat_id=MAIN_CHANNEL_ID,
        item_id=item_id,
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text="Post created successfully", )