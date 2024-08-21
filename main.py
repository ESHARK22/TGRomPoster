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
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
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



tg_app  = ApplicationBuilder()             \
            .token(config.TG_BOT_TOKEN)     \
            .build()

# Add the start command
tg_app.add_handler(CommandHandler("start", cmd_start))

# Run the app
tg_app.run_polling()
