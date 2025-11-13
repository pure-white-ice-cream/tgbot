import logging
import os
import random

from telegram import Update
from telegram.ext import ContextTypes

channel_id = "@xgsjw"
max_attempts = 5  # 尝试次数，避免无限循环
BIGIN_ID = os.environ.get("BIGIN_ID", "0")
END_ID = os.environ.get("END_ID", "0")
BAN_IDS = os.environ.get("BAN_IDS", "0")
if BAN_IDS.strip():
    BAN_IDS = {int(x.strip()) for x in BAN_IDS.split(",") if x.strip()}
else:
    BAN_IDS = set()

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    last_exception = ''
    for _ in range(max_attempts):
        message_id = None
        try:
            while message_id in BAN_IDS or message_id is None:
                message_id = random.randint(int(BIGIN_ID), int(END_ID))
            await context.bot.forward_message(
                chat_id=chat_id,
                from_chat_id=channel_id,
                message_id=message_id
            )
            return  # 成功就返回
        except Exception as e:
            last_exception = e
            logging.warning(f"获取随机消息失败: https://t.me/{channel_id[1:]}/{message_id}")
            continue
    # 如果多次尝试都失败
    await context.bot.send_message(chat_id, f"获取随机消息失败: {last_exception}")