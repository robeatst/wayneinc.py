# 🤖 Discord Bot (Python + Koyeb)

Простой Discord-бот, написанный на Python с использованием `discord.py`, готовый к деплою на **Koyeb**.

## 🚀 Как развернуть

1. Создай Discord-приложение на [Discord Developer Portal](https://discord.com/developers/applications)
2. Создай бота, скопируй токен и добавь его в переменные окружения:
   ```
   DISCORD_TOKEN=твой_токен
   ```
3. Разверни на [Koyeb](https://www.koyeb.com/) из GitHub:
   - **Run command:** `python main.py`
   - **Service type:** `worker`
   - Добавь переменную окружения `DISCORD_TOKEN`
4. После деплоя бот автоматически запустится и будет доступен онлайн.

## 🧠 Команды
- `/ping` — проверка отклика бота
