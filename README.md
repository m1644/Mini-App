# Telegram Pizza Mini App + Bot

Готовый проект Mini App (как @DurgerKingBot) + Telegram-бот на aiogram v3. 

- Бот присылает приветствие с кнопкой Mini App
- Вся логика оформления заказа в Mini App (веб-приложение)
- После оформления заказ отправляется в чат с пользователем и менеджеру в канал

## Быстрый старт (Replit)
1. Создайте репл Python и загрузите файлы проекта
2. Создайте `.env` по образцу `.env.example` и заполните:
   - `BOT_TOKEN` — токен бота
   - `MANAGER_CHAT_ID` — id канала/чата менеджера (бот должен быть админом там)
   - `WEBAPP_URL` — публичный URL вашего Replit (например, https://myproject.username.repl.co/)
   - `PORT` — 8000 (по умолчанию)
3. Установите зависимости: `pip install -r requirements.txt`
4. Запустите: `python main.py`
5. Откройте бота в Telegram и отправьте `/start`

## Локальный запуск
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Скопируйте `.env.example` в `.env` и заполните значения
4. Запустите `python main.py`

### Тестирование на локальном ПК (без Telegram)
- Установите в `.env` переменную `RUN_WEB_ONLY=true` и (по желанию) оставьте `WEBAPP_URL=http://localhost:8000`.
- Откройте в браузере `http://localhost:8000`.
- Mini App будет получать меню с `/api/menu` и отправлять оформление заказа POST запросом на `/api/order`.
- В Telegram-режиме Mini App отправляет данные через `Telegram.WebApp.sendData`, а локально — через REST API.

### Запуск Telegram-бота (опционально)
- Установите зависимости для бота: `pip install -r bot-requirements.txt`
- Укажите `BOT_TOKEN` и, при необходимости, `MANAGER_CHAT_ID` в `.env`.
- Установите `RUN_WEB_ONLY=false` или просто задайте `BOT_TOKEN`.
- Запустите `python main.py` и отправьте `/start` боту в Telegram.

## Структура
- `main.py` — запуск FastAPI и aiogram (параллельно)
- `bot_config.py` — меню, изображения, промокоды
- `webapp/` — фронтенд Mini App
  - `index.html`
  - `styles.css`
  - `app.js`

## Примечания
- Mini App внутри Telegram вызывает `Telegram.WebApp.sendData`, бот получает данные и отправляет заказ вам и менеджеру.
- Цены/товары идентичны между Mini App и ботом — источник единый (`bot_config.py`).