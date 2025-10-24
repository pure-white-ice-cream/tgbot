import os
import logging
import requests
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageFilter
from telegram import BotCommand, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()  # 只在本地载入 .env
token = os.getenv("TG_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong!")


async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 获取用户发送的图片列表，选择最大的一张
    photo = update.message.reply_to_message.photo[-1]

    # 下载图片到内存
    photo_file = await photo.get_file()
    bio = BytesIO()
    await photo_file.download_to_memory(out=bio)

    img_file = Image.open(bio)
    # 示例处理：灰度 + 模糊
    img_file = img_file.convert("L").filter(ImageFilter.GaussianBlur(2))

    # 保存处理后的图片到内存
    out_bio = BytesIO()
    img_file.save(out_bio, format="PNG")
    out_bio.seek(0)

    # 发送处理后的图片回用户
    await update.message.reply_photo(photo=out_bio)


async def yy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_quote())


def get_random_quote():
    url = "https://v1.hitokoto.cn/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        quote = (data.get('hitokoto') or '').strip()
        source = (data.get('from') or '').strip()
        author = (data.get('from_who') or '').strip()

        if source == author or not source:
            return f"{quote} — {author or '未知'}"
        else:
            return f"{quote} — {source}·{author or '未知'}"

    except requests.RequestException as e:
        return f"获取名言失败: {e}"


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    # 设置命令列表和说明
    application.bot.set_my_commands([
        BotCommand("start", "启动机器人"),
        BotCommand("help", "显示帮助信息"),
        BotCommand("echo", "回复你发送的文本")
    ])

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    ping_handler = CommandHandler('ping', ping)
    application.add_handler(ping_handler)

    img_handler = CommandHandler('img', img)
    application.add_handler(img_handler)

    yy_handler = CommandHandler('yy', yy)
    application.add_handler(yy_handler)

    application.run_polling()
