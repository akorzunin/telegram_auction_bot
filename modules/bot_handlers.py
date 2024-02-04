from telegram import (
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InputMediaPhoto,
)
from telegram.ext import CallbackContext
import logging
import json
import requests
from modules.bot_callbacks import (
    get_price_callback,
    attend_callback,
    price_increment_callback,
)


randomPImageUrl = "https://picsum.photos/1200"


def user_white_list():
    #     # white list of users
    #     # if update.effective_chat.username not in allowedUsernames:
    #     #     context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
    pass


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    # OLD CALLBACKS TODO remove later

    if "callback1" in query:
        logging.info("callback1")
        print(update)
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text="Вы приняли участие в аукционе",
        )

    if "callback2" in query:
        logging.info("callback2")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="callback2 message"
        )

    if "new_msg" in query:
        logging.info("new_msg")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="new_msg message"
        )

    # NEW CALLBACKS

    if "get_price_callback" in query:
        item_id = int(query[query.find("id=") + len("id=") :])
        get_price_callback(
            update=update,
            context=context,
            item_id=item_id,
        )
    if "attend_callback" in query:
        item_id = int(query[query.find("id=") + len("id=") :])
        if __debug__:  # TODO read debug from .env
            logging.info("attend_callback")
            # context.bot.send_message(
            #     chat_id=ADMIN_CHAT_ID,
            #     text=f'attend_callback for item_id: {item_id}'
            # )
        attend_callback(
            update=update,
            context=context,
            item_id=item_id,
        )

    if "price_increment" in query:
        # parse out item_id and value into dict
        json_dict = "".join(query.split(" ")[1:])
        callback_data = json.loads(json_dict)
        price_increment_callback(
            update=update,
            context=context,
            item_id=callback_data["id"],
            price_increment=callback_data["val"],
        )
