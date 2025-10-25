import logging
import os

from dotenv import load_dotenv
from telegram import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, \
    BotCommandScopeAllChatAdministrators
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from command import xg, start


async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "打招呼"),
        BotCommand("xg", "获取随机雪糕图片"),
    ]

    # 删除所有旧命令作用域
    await application.bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await application.bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    await application.bot.delete_my_commands(scope=BotCommandScopeAllChatAdministrators())
    await application.bot.delete_my_commands(scope=BotCommandScopeDefault())

    # 设置命令
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