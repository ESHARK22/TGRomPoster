from telegram import Message
from telegram.constants import ParseMode
from textwrap import dedent


async def reply(reply_to_message: Message, text: str, photo: str | None = None, parse_mode: ParseMode | None = None):
    if photo:
        await reply_to_message.reply_photo(
            photo,
            caption=dedent(text),
            parse_mode=parse_mode
        )
    else:
        await reply_to_message.reply_text(
            dedent(text),
            parse_mode=parse_mode
        )
