# tgbot

## 使用方法
- 向 https://t.me/BotFather 获取你的机器人令牌
- 安装 docker
- 编写 docker-compose.yml 文件，内容如下：
```yaml
services:
  tgbot:
    image: purewhiteicecream/tgbot:latest
    container_name: tgbot
    restart: always
    environment:
      - "TG_BOT_TOKEN= 填写机器人令牌, 形如 4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc"
      - "BEGIN_ID=8"
      - "END_ID=513"
      - "BAN_IDS=34, 113, 114, 171, 172, 173, 174, 175, 176, 177, 178, 179, 185, 235, 375, 376, 456"
```
- 运行 `docker-compose up -d` 启动服务

## 技术栈
- [Python](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/)

# 部署
- [docker](https://www.docker.com/)