import asyncio
import os
import logging
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application

from command import yy, img

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong!")


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        ("start", "启动机器人"),
        ("ping", "测试机器人是否在线"),
        ("img", "图片转为灰色模糊"),
        ("yy", "一言")
    ])


def main():
    load_dotenv()  # 只在本地载入 .env
    token = os.getenv("TG_BOT_TOKEN")

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token(token).post_init(post_init).build()

    # 注册 Handler
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    application.add_handler(CommandHandler('img', img.command))
    application.add_handler(CommandHandler('yy', yy.command))

    application.run_polling()

if __name__ == '__main__':
    main()