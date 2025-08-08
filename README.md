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