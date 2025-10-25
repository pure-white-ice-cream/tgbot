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
      - TG_BOT_TOKEN= 填写机器人令牌, 形如 4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc
```
- 运行 `docker-compose up -d` 启动服务

## 技术栈
- [Python](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/)

# 部署
- [docker](https://www.docker.com/)