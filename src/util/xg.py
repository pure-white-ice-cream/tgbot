import logging
import random

from telegram import Update
from telegram.ext import ContextTypes

channel_id = "@xgsjw"
max_attempts = 5  # 尝试次数，避免无限循环
BLACKLIST_IDS = {34, 113, 114, 171, 172, 173, 174, 175, 176, 177, 178, 179, 185, 235, 375, 376}  # 已知的无效或视频消息ID

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    last_exception = ''
    for _ in range(max_attempts):
        message_id = None
        try:
            while message_id in BLACKLIST_IDS or message_id is None:
                message_id = random.randint(8, 492)
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