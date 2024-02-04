import logging
from typing import Dict

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ParseMode,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.error import TimedOut
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

(
    TEXT_CHOISE,
    TYPING_REPLY,
    TYPING_CHOICE,
    PHOTO_CHOICE,
    ENTER_TITLE,
    ENTER_DESCRIPTION,
    ENTER_PRICE,
) = range(21 - 15 + 1)
POST_CHANNEL_ID = 503131177  # my direct message
# POST_CHANNEL_ID = -1001663892384 # actual channel id

reply_keyboard = [
    ["Add photo", "Add title"],
    ["Add description", "Add price"],
    ["Something else..."],
    ["Preview", "Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


def new_post(update: Update, context: CallbackContext) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    # init empty list to store dicts w/ info about each uploaded photo
    context.user_data["photos"] = []

    reply_text = "Initiate conversation: new post "
    # if context.user_data:
    #     reply_text += (
    #         f"Current data: {', '.join(context.user_data.keys())}."
    #     )
    # else:
    reply_text += "Enter title"
    update.message.reply_text(reply_text, reply_markup=markup)

    return ENTER_TITLE


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text.lower().replace("add ", "").title()
    logging.info(f"{text}")
    context.user_data["choice"] = text
    if context.user_data.get(text):
        reply_text = f"New data: {text}\nCurrent data: {context.user_data[text]}"
    else:
        reply_text = f"New data: {text}\nEnter text:"
    update.message.reply_text(reply_text)
    # context.bot.s

    return TYPING_REPLY


def recieve_title(update: Update, context: CallbackContext) -> int:

    context.user_data["Title"] = update.message.text
    reply_text = "Enter description"
    update.message.reply_text(reply_text)

    return ENTER_DESCRIPTION


def recieve_description(update: Update, context: CallbackContext) -> int:

    context.user_data["Description"] = update.message.text
    reply_text = "Enter price"
    update.message.reply_text(reply_text)

    return ENTER_PRICE


def recieve_price(update: Update, context: CallbackContext) -> int:

    context.user_data["Price"] = update.message.text
    reply_text = "Upload photo"
    update.message.reply_text(reply_text)

    return PHOTO_CHOICE


def photo_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text.lower().replace("add ", "").title()

    logging.info(f"{text}")
    if context.user_data.get("photos"):
        reply_text = f'New data: {text}\nCurrent photos: {context.user_data["photos"]}'
    else:
        reply_text = f"New data: {text}\nEnter photo:"
    update.message.reply_text(reply_text)

    return PHOTO_CHOICE


def photo_upload(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    # get data from user message
    caption = update.message.caption
    file_id = update.message.photo[-1].file_id
    file_dl_link = update.message.photo[-1].get_file()["file_path"]

    # put data to context
    context.user_data["photos"].append(
        dict(
            caption=caption,
            file=update.message.photo[-1],
            file_dl_link=file_dl_link,
        )
    )

    logging.debug(f'{update.message.photo[-1].get_file()["file_path"]}')
    logging.debug(f"{update.message.photo[-1]}, {type(update.message.photo[-1])}")
    logging.debug(f'{context.user_data["photos"]}')

    if context.user_data.get(file_id):
        reply_text = f"New data: {file_id}\nCurrent photo: {context.user_data[file_id]}"
    else:
        # TODO split to diff lines of code
        reply_text = f"Photo successfully received\n Caption: {caption}\n file id: {file_id}\n file_dl_link: {file_dl_link}"
    update.message.reply_text(reply_text)
    # assert 0
    return TEXT_CHOISE


def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    text = update.message.text
    category = context.user_data["choice"]
    context.user_data[category] = text.lower()
    del context.user_data["choice"]

    update.message.reply_text(
        "Current data:" f"{facts_to_str(context.user_data)}",
        reply_markup=markup,
    )

    return TEXT_CHOISE


def show_data(update: Update, context: CallbackContext) -> None:
    """Display the gathered info."""
    update.message.reply_text(f"Current post data: {facts_to_str(context.user_data)}")
    # send appended photos
    context.bot.send_media_group(
        # chat_id=-1001663892384,
        chat_id=update.effective_chat.id,
        media=[
            InputMediaPhoto(
                media=i["file"],
                # caption=i['caption']
            )
            for i in context.user_data["photos"]
        ],
    )
    return TEXT_CHOISE


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(context.user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def upload_post(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    update.message.reply_text(
        f"Data to be uploaded: {facts_to_str(context.user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )
    ### create DB item here

    ### send post to channel
    send_post_to_channel(update, context, POST_CHANNEL_ID, 1)
    return ConversationHandler.END


def send_post_to_channel(
    update: Update, context: CallbackContext, chat_id: int, item_id
):
    """require
    context.user_data['Title']
    context.user_data['Description']
    context.user_data['Price']
    """

    def fix_md(text: str) -> str:
        return text.replace(".", "\.").replace("-", "\-")

    buttons = [
        [
            InlineKeyboardButton(
                "Get price", callback_data=f"get_price_callback id={item_id}"
            )
        ],
        [InlineKeyboardButton("Attend", callback_data=f"attend_callback id={item_id}")],
    ]
    description = fix_md(context.user_data["Description"])
    title = fix_md(context.user_data["Title"])
    text = f"""
    *{title}*
    {description}

    ~Price: {int(context.user_data['Price'])}~
    """

    msg = context.bot.send_media_group(
        chat_id=chat_id,
        media=[
            InputMediaPhoto(
                media=i["file"],
                # caption=i['caption']
            )
            for i in context.user_data["photos"]
        ],
    )
    context.bot.edit_message_caption(
        chat_id=msg[0].chat_id,
        message_id=msg[0].message_id,
        caption=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    try:
        context.bot.send_message(
            chat_id=chat_id,
            text=f'*{context.user_data["Title"]}* actions',
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except TimedOut:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Time out error: post message too long or not uploaded fast enough",
        )

    # logging.info(f'{context.user_data}')


post_upload_conversation = ConversationHandler(
    entry_points=[CommandHandler("new_post", new_post)],
    states={
        TEXT_CHOISE: [
            MessageHandler(
                Filters.regex("^(Add title|Add description|Add price)$"), regular_choice
            ),
            MessageHandler(Filters.regex("^(Add photo)$"), photo_choice),
            MessageHandler(Filters.regex("^(Preview)$"), show_data),
            MessageHandler(Filters.regex("^Something else...$"), custom_choice),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex("^(Done)$")),
                regular_choice,
            )
        ],
        PHOTO_CHOICE: [
            MessageHandler(
                Filters.photo & ~(Filters.command | Filters.regex("^(Done)$")),
                photo_upload,
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex("^Done$")),
                received_information,
            ),
        ],
        ENTER_TITLE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex("^Done$")),
                recieve_title,
            ),
        ],
        ENTER_DESCRIPTION: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex("^Done$")),
                recieve_description,
            ),
        ],
        ENTER_PRICE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex("^Done$")),
                recieve_price,
            ),
        ],
    },
    fallbacks=[
        MessageHandler(Filters.regex("^Done$"), upload_post),
        # MessageHandler(Filters.regex('^Preview$'), show_data),
        # MessageHandler(Filters.regex('^$'), show_data),
    ],
    name="my_conversation",
    # persistent=True,
)
