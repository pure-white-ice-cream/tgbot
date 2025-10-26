import logging
import random
from uuid import uuid4

from telegram import Update, InlineQueryResultPhoto
from telegram.ext import ContextTypes

channel_id = "@xgsjw"
max_attempts = 5  # 尝试次数，避免无限循环
BLACKLIST_IDS = {34, 113, 114, 171, 172, 173, 174, 175, 176, 177, 178, 179, 235}  # 已知的无效或视频消息ID


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


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()  # 用户输入的文字

    # 用户什么都没输入
    if not query:
        results = []
        for _ in range(1):
            try:
                message_id = None
                while message_id in BLACKLIST_IDS or message_id is None:
                    message_id = random.randint(8, 492)
                results.append(
                    InlineQueryResultPhoto(
                        id=str(uuid4()),
                        photo_url=f"https://t.me/{channel_id[1:]}/{message_id}",
                        thumbnail_url="https://youke1.picui.cn/s1/2025/10/26/68fe01bebe21d.jpg",
                        caption=f"https://t.me/{channel_id[1:]}/{message_id}",
                    )
                )
            except Exception as e:
                last_exception = e
                continue
        await update.inline_query.answer(results, cache_time=5)
        return
