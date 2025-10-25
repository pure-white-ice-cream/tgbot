import logging
import os

from dotenv import load_dotenv
from telegram import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, \
    BotCommandScopeAllChatAdministrators, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from command import start, get, xg


async def post_init(application: Application) -> None:
    bot: Bot = application.bot  # type: ignore
    commands = [
        BotCommand("start", "打招呼"),
        BotCommand("get", "获取用户或群组信息"),
        BotCommand("xg", "获取随机雪糕图片"),
    ]

    # 删除所有旧命令作用域
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    await bot.delete_my_commands(scope=BotCommandScopeAllChatAdministrators())
    await bot.delete_my_commands(scope=BotCommandScopeDefault())

    # 设置命令
    await bot.set_my_commands(commands)


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
    application.add_handler(CommandHandler('get', get.command))
    application.add_handler(CommandHandler('xg', xg.command))

    application.run_polling()


if __name__ == '__main__':
    main()