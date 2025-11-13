# 使用轻量级官方镜像
FROM python:3.14-slim AS base

# 禁用 Python 缓冲与 pip cache，提升容器性能
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    TG_BOT_TOKEN=0 \
    BIGIN_ID=0 \
    END_ID=0 \
    BAN_IDS=0

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如需编译某些包）
# 单独一层方便缓存复用
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# 仅复制 requirements.txt 以最大化利用缓存
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用源代码（最后复制，避免频繁失效缓存）
COPY src/ ./src

# 默认执行命令
CMD ["python", "src/app.py"]
