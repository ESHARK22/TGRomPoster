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

from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    filters
)

from helper_msg import reply
import config

# Setup logging
logger = logging.getLogger("RomManager")
coloredlogs.install(level='DEBUG', logger=logger)
(debug, info, warn, error, fatal) = \
    ( logger.debug, logger.info, logger.warn, logger.error, logger.fatal )

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    debug(f"Start command was run.")
    debug(f" > Update: {update}")

    if not update.message:
        error("> No message associated with this update!?!")
        return

    await reply(update.message, """
        This is a wip bot to generate ROM release posts
        Run /new_post to try it out :D (probably wont work yet :/)
        """
    )

async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resets user_data, and ends the conversation."""
    if not context.user_data:
        raise Exception("No user data associated with this context!?!")
    if not update.message:
        raise Exception("No message associated with this update!?!")
    if not update.message.from_user:
        raise Exception("No from user was associated with this update!?!")

    user_data = context.user_data
    user_name = update.message.from_user.username
    user_id = update.message.from_user.id
    message = update.message

    user_data["post"] = {}

    await reply(message, """
        Post cancelled!
        All the saved data from this post has been discarded
        """
    )
    return ConversationHandler.END

async def cmd_new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error("Command: /new_post - TODO!")

async def received_rom_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error("ConvState: RomName - TODO!")

class PostConversationState:
    ROM_NAME    = 1
    ROM_BANNER  = 2
    DEVICE_NAME = 3
    LINKS       = 4
    POST        = 5

new_post_conversation_handler = ConversationHandler (
    entry_points = [
        CommandHandler("new_post", cmd_new_post)
    ],
    states = {
        PostConversationState.ROM_NAME: [
            MessageHandler(filters.TEXT, received_rom_name)
        ]
    },
    fallbacks = [
        CommandHandler("cancel", cmd_cancel)
    ]
)

tg_app  = ApplicationBuilder()             \
            .token(config.TG_BOT_TOKEN)     \
            .build()

# Add the start command, and the conversation handler
tg_app.add_handler(CommandHandler("start", cmd_start))
tg_app.add_handler(new_post_conversation_handler)

# Run the app
tg_app.run_polling()
