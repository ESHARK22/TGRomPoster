from telegram import Message
from textwrap import dedent


async def reply(reply_to_message: Message, text: str):
    await reply_to_message.reply_text(dedent(text))
