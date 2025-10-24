# 使用官方 Python 镜像
FROM python:3.14-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件（不包括 .env）
COPY requirements.txt .
COPY src ./src

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 预留环境变量（可以在运行时覆盖）
ENV TG_BOT_TOKEN=""

# 默认运行命令
CMD ["python", "src/app.py"]
