import random
from uuid import uuid4

from telegram import Update, InlineQueryResultCachedPhoto, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

from . import xg
from . import yy

channel_id = xg.channel_id
max_attempts = xg.max_attempts
BLACKLIST_IDS = xg.BLACKLIST_IDS


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()  # 用户输入的文字

    if query.startswith("yy"):
        parts = query.split(maxsplit=1)  # 只分割一次
        lang = parts[1] if len(parts) > 1 else ""  # 提取 'zh'
        results = []

        for i in range(5):
            message = yy.get_random_paimon_quote(lang)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=message,
                    input_message_content=InputTextMessageContent(message),
                    thumbnail_url="https://webstatic.mihoyo.com/upload/static-resource/2023/05/31/5280971436689ca024c98a9d3a2b8944_2776048451394759406.png",
                )
            )
        await update.inline_query.answer(results, cache_time=5)
        return

    if query.startswith("xg"):

        results = []

        for i in range(5):
            message_id = None
            while message_id in BLACKLIST_IDS or message_id is None:
                message_id = random.randint(8, 492)

            message = await context.bot.forward_message(
                chat_id=-1003260240392,
                from_chat_id=channel_id,
                message_id=message_id,
            )

            results.append(
                InlineQueryResultCachedPhoto(
                    id=str(uuid4()),
                    photo_file_id=message.photo[-1].file_id,
                )
            )

        await update.inline_query.answer(results, cache_time=5)
        return

    # 用户什么都没输入
    if not query:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="💡 输入 xg 获取随机雪糕图片",
                description=f"你可以输入{context.bot.name} xg 来获取随机雪糕图片 🍦",
                input_message_content=InputTextMessageContent(
                    f"你可以输入{context.bot.name} xg 来获取随机雪糕图片 🍦"
                ),
                thumbnail_url="https://upload-bbs.miyoushe.com/upload/2020/06/01/76387920/375c32d3a67546ec40f2c6531a6483f6_8288198106530274988.png?x-oss-process=image//resize,s_600/quality,q_80/auto-orient,0/interlace,1/format,png",
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="💡 输入 yy 获取随机派蒙一言",
                description=f"你可以输入{context.bot.name} yy 来获取随机派蒙一言 💘",
                input_message_content=InputTextMessageContent(
                    f"你可以输入{context.bot.name} yy 来获取随机派蒙一言 💘"
                ),
                thumbnail_url="https://webstatic.mihoyo.com/upload/static-resource/2023/05/31/5280971436689ca024c98a9d3a2b8944_2776048451394759406.png",
            ),
        ]
        await update.inline_query.answer(results, cache_time=5)
        return
