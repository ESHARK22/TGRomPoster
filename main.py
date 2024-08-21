# This is a bot to allow builders to create and post ROM releases to the relevant device channel

# Data: Post : {
#   "rom_name": "Leaf OS"
#   "rom_banner_file_id": None|FileID
#   "device_name": "starlte "
#   "links": [
#       "[]()",
#       "[]()"
#   ]
#   "MessageID": MessageId|None -> used to edit the message
# }

# Data: Device Topic Info: {
#   "device_name": {
#       "TopicThreadID": "topic_id
#       "Allowed_Posters": [
#           "a_id",
#            "b_id"
#       ]
#   }
# }

import logging

import coloredlogs
import config
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

from helper_errors import (MissingMessageDataError,
                           MissingMessageFromUserError, MissingUserDataError)
from helper_links import is_valid_link
from helper_msg import reply

# Setup logging
logger = logging.getLogger("RomManager")
coloredlogs.install(level="DEBUG", logger=logger)
(debug, info, warn, error, fatal) = (
    logger.debug,
    logger.info,
    logger.warn,
    logger.error,
    logger.fatal,
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    debug(f"Start command was run.")
    debug(f" > Update: {update}")

    if not update.message:
        raise MissingMessageDataError()

    await reply(
        update.message,
        """
        This is a wip bot to generate ROM release posts
        Run /new_post to try it out :D (probably wont work yet :/)
        """,
    )


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resets user_data, and ends the conversation."""
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    user_data["post"] = {}

    await reply(
        message,
        """
        Post cancelled!
        All the saved data from this post has been discarded
        """,
    )
    return ConversationHandler.END


async def cmd_new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation, and asks for the ROM name"""

    # Make sure everything we need exists

    # We dont need user_data, since it doesnt exist yet...
    # if not context.user_data:
    #     raise MissingUserDataError()

    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    info(f"{user_name}({user_id}) started a new release")

    # Set the user data to empty
    user_data["post"] = {}  # pyright: ignore

    await reply(
        message,
        """
        Welcome to the ROM post generator by @eshark22

        You can canel this post at any time using /cancel

        Part 1/5-todo) Send the name of the ROM
        """,
    )
    return PostConversationState.ROM_NAME


async def received_rom_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the rom name, and ask for the ROM banner (image, or skip)"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    # Get the rom name that was sent
    rom_name = update.message.text

    # Make sure the rom name exists
    if not rom_name:
        await reply(
            message,
            f"""
            No Rom name was provided!?!

            Part 1/5-todo) Try sending a rom name again
        """,
        )
        return PostConversationState.ROM_NAME

    # Save the rom name
    user_data["post"]["rom_name"] = rom_name
    info(f"{user_name}({user_id}) set '{rom_name}' as the rom name")

    await reply(
        message,
        f"""
        Set "{rom_name}" as the ROM name

        Part 2/5-todo) Send either an image to set as a banner, or send /skip
    """,
    )
    return PostConversationState.ROM_BANNER


async def received_rom_banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the ROM banner image, and ask for the device name"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    # We only need the file id of the banner that was sent
    rom_image_id = update.message.photo[-1].file_id

    if not rom_image_id:
        await reply(
            message,
            f"""
            No Rom banner was provided!?!

            Part 1/5-todo) Try sending either an image to set as a banner, or send /skip
        """,
        )
        return PostConversationState.ROM_BANNER

    # Save the banners file id
    user_data["post"]["rom_banner_file_id"] = rom_image_id

    await reply(
        message,
        f"""
        Saved the rom banner

        Part 3/5-todo) Send the device name
    """,
    )
    return PostConversationState.DEVICE_NAME


async def cmd_skip_rom_banner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set the ROM banner image as None, and ask for the device name"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    # Set the banner id to None
    user_data["post"]["rom_banner_file_id"] = None

    await reply(
        message,
        f"""
        Set the banner photo to None

        Part 3/5-todo) Send the device name
    """,
    )
    return PostConversationState.DEVICE_NAME


async def received_device_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the device name, and ask for the links"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    device_name = update.message.text
    if not device_name:
        error("No device names were provided!?!")
        await reply(
            message,
            """
            No device names were provided!?!
            Try again...
        """,
        )
        return PostConversationState.DEVICE_NAME

    user_data["post"]["device_name"] = device_name

    await reply(
        message,
        f"""
        Set the device name as {device_name}

        Part 4/5-todo) Send the links in the following format: [URL](http://www.example.com/)
        Multiple links can be split by new lines'
    """,
    )
    return PostConversationState.LINKS


async def received_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the ROM banner image, and ask for the device name"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    # Get what the user sent
    links = update.message.text
    if not links:
        error("No download links were provided!?!")
        await reply(
            message,
            """
            No download links were provided!?!
            Try again...
        """,
        )
        return PostConversationState.LINKS

    # Turn it into a list
    if "\n" in links:
        links = links.split("\n")
    else:
        links = [links]

    # Check each link that was passed
    for link in links:
        if not is_valid_link(link):
            error(f"Invalid link was provided: {link}")
            await reply(
                message,
                """
                Invalid download link was provided
                Try again...
            """,
            )
            return PostConversationState.LINKS

    user_data["post"]["links"] = links
    post = user_data["post"]
    link_str = "\n"
    for link in links:
        link_str += f"      -> {link}"
        link_str += "\n"

    await reply(
        update.message,
        f"""
        Yay, those were valid links...

        Here is the current info:
        ```
        Rom Name: {post["rom_name"]}
        Rom banner (file id): {post["rom_banner_file_id"]}
        Device Name: {post["device_name"]}
        Links: {link_str}
        ```
        Send /post to create this post
        or /cancel to cancel it
    """,
    )

    return PostConversationState.POST


async def cmd_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the ROM banner image, and ask for the device name"""

    # Make sure everything we need exists
    if not context.user_data:
        raise MissingUserDataError()
    if not update.message:
        raise MissingMessageDataError()
    if not update.message.from_user:
        raise MissingMessageFromUserError()

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message
    post_data = user_data["post"]

    info(post_data)


class PostConversationState:
    ROM_NAME = 1
    ROM_BANNER = 2
    DEVICE_NAME = 3
    LINKS = 4
    POST = 5


new_post_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("new_post", cmd_new_post)],
    states={
        PostConversationState.ROM_NAME: [
            MessageHandler(filters.TEXT, received_rom_name)
        ],
        PostConversationState.ROM_BANNER: [
            MessageHandler(filters.PHOTO, received_rom_banner),
            CommandHandler("skip", cmd_skip_rom_banner),
        ],
        PostConversationState.DEVICE_NAME: [
            MessageHandler(filters.TEXT, received_device_name)
        ],
        PostConversationState.LINKS: [MessageHandler(filters.TEXT, received_links)],
        PostConversationState.POST: [CommandHandler("post", cmd_post)],
    },
    fallbacks=[CommandHandler("cancel", cmd_cancel)],
)

tg_app = ApplicationBuilder().token(config.TG_BOT_TOKEN).build()

# Add the start command, and the conversation handler
tg_app.add_handler(CommandHandler("start", cmd_start))
tg_app.add_handler(new_post_conversation_handler)

# Run the app
tg_app.run_polling()
