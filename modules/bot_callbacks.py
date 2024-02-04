from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import CallbackContext

from modules import api_handler
from settings.env import API_ENDPOINT as ENDPOINT
from utils.dqdict import Dqdict as dqdict


def get_price_callback(update: Update, context: CallbackContext, item_id: int):
    """return to user price of item in DM if it is not sold
    if item sold then tell that to user in DM
    """
    item_data = api_handler.read_item_by_id(
        id=item_id,
        endpoint=ENDPOINT,
    )
    # to get into dm use update.effective_user.id
    text = f"""
    Info about item: {item_data['title']}

    Description:
    {item_data['description']}

    Price: {item_data['price']}
    Current owner: {'None' if item_data['owner_id'] == 0 else item_data['owner_id']}

    Item currently is {'sold' if item_data['is_sold'] else 'not sold'}

    """
    # send msg to user
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
    )


def attend_callback(update: Update, context: CallbackContext, item_id: int):
    """Add user to auction an tell that in DM if item is not sold
    if item sold then tell that to user in DM
    """
    # get user nickname from context
    username = update.effective_user.username
    # get user interface language
    # language_code = update.effective_user.language_code
    # check if that user already exists in DB
    r = api_handler.get_user_by_username(
        username=username,
        endpoint=ENDPOINT,
    )
    # handle r.status_code > 399 TODO
    user_data = r.json()
    if user_data is not None:
        # user exist
        # get user id
        r = api_handler.get_user_by_username(
            username=username,
            endpoint=ENDPOINT,
        )
        user_data = r.json()
        # user_id = user_data["id"]

    elif user_data is None:
        # create user
        r = api_handler.create_user(
            username=username,
            endpoint=ENDPOINT,
        )
        if r.status_code < 399:
            # user created
            user_data = r.json()
            # user_id = user_data["id"]
        # TODO handle status_code > 399

    item = api_handler.read_item_by_id(
        id=item_id,
        endpoint=ENDPOINT,
    )
    # send msg to user
    # https://www.figma.com/file/7Rmtk9aiGvOyfKEPJMqfxG/bot-alg?node-id=55%3A1516

    buttons = [
        [
            InlineKeyboardButton(
                "+100", callback_data=f"price_increment {dqdict(id=item_id, val=100)}"
            ),
            InlineKeyboardButton(
                "+500", callback_data=f"price_increment {dqdict(id=item_id, val=500)}"
            ),
        ],
        [
            InlineKeyboardButton(
                "Get price", callback_data=f"get_price_callback id={item_id}"
            )
        ],
    ]
    text = f"""
    Attent in auction?
    Продолжается аукцион
    на лот {item['title']}
    id: {item_id}

    Текущая цена {item['price']}
    """

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def price_increment_callback(
    update: Update, context: CallbackContext, item_id: int, price_increment: int
):
    # get user id name from update
    username = update.effective_user.username
    r = api_handler.get_user_by_username(username, ENDPOINT)
    user_id = r.json()["id"]
    # change item: owner id and new price(price_increment)
    data = api_handler.reassign_item(
        item_id=item_id,
        user_id=user_id,
        endpoint=ENDPOINT,
        price_increment=price_increment,
    )
    buttons = [
        [
            InlineKeyboardButton(
                "+100", callback_data=f"price_increment {dqdict(id=item_id, val=100)}"
            ),
            InlineKeyboardButton(
                "+500", callback_data=f"price_increment {dqdict(id=item_id, val=500)}"
            ),
        ],
        [
            InlineKeyboardButton(
                "Get price", callback_data=f"get_price_callback id={item_id}"
            )
        ],
    ]
    text = f"""
    Item: {data['title']} id: {data['id']}
    was successfully reassigned to user {username}
    Current price: {data['price']}

    """
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
