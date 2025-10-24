import requests
from telegram import Update
from telegram.ext import ContextTypes


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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