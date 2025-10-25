import random

from telegram import Update
from telegram.ext import ContextTypes


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    channel_id = "@xgsjw"
    max_attempts = 5  # 尝试次数，避免无限循环
    last_exception = ''
    for _ in range(max_attempts):
        try:
            # 随机生成一个 message_id（这里最好是你自己知道的范围）
            message_id = random.randint(1, 500)
            await context.bot.forward_message(
                chat_id=chat_id,
                from_chat_id=channel_id,
                message_id=message_id
            )
            return  # 成功就返回
        except Exception as e:
            last_exception = e
            continue
    # 如果多次尝试都失败
    await context.bot.send_message(chat_id, f"获取随机消息失败: {last_exception}")
