from telegram import Update, User
from telegram.error import Forbidden, BadRequest, NetworkError
from telegram.ext import ContextTypes


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    message = update.effective_message

    target_user: User | None = None
    arg = context.args[0] if context.args else None

    # ========== 没参数且有回复 ==========
    if not arg and message.reply_to_message:
        target_user = message.reply_to_message.from_user

    # ========== /get me ==========
    elif arg and arg.lower() == "me":
        target_user = update.effective_user

    # 用户信息展示
    if target_user:
        user = target_user
        bio = "无法获取简介（Bot 无权限查看）"
        try:
            chat_info = await bot.get_chat(user.id)
            if chat_info.bio:
                bio = chat_info.bio
        except (Forbidden, BadRequest):
            # 这些错误代表用户不允许获取资料或不存在，不必记录
            pass
        except NetworkError:
            bio = "网络错误，暂时无法获取简介"

        is_bot = "✅" if user.is_bot else "❎"
        is_premium = "✅" if user.is_premium else "❎"

        text = (
            f"🧍‍♂️ 用户信息\n"
            f"🆔ID: <code>{user.id}</code>\n"
            f"🎨昵称: {user.full_name}\n"
            f"🏷用户名: {user.name}\n"
            f"🌐用户语言: {user.language_code}\n"
            f"🖋简介:\n{bio}\n\n"

            f"🤖机器人: {is_bot}\n"
            f"💎高级用户: {is_premium}\n"
        )
        await message.reply_text(text, parse_mode="HTML")
        return

    # 没有目标时提示
    await message.reply_text("❗用法:\n"
                             "/get me — 获取自己信息\n"
                             "或回复一条消息再输入 /get 获取被引用对象信息")
