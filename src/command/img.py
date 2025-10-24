from io import BytesIO
from PIL import Image, ImageFilter
from telegram import Update
from telegram.ext import ContextTypes


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
