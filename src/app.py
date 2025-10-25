import os
import logging

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application

from command import xg, start


async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "打招呼"),
        BotCommand("xg", "获取随机雪糕图片"),
    ]
    await application.bot.set_my_commands(commands)


def main():
    load_dotenv()  # 只在本地载入 .env
    token = os.getenv("TG_BOT_TOKEN")

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token(token).post_init(post_init).build()

    # 注册 Handler
    application.add_handler(CommandHandler('start', start.command))
    application.add_handler(CommandHandler('xg', xg.command))

    application.run_polling()


if __name__ == '__main__':
    main()