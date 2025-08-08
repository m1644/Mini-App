import os
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import uvicorn

from dotenv import load_dotenv

from bot_config import MENU, PROMO_CODES, ITEM_ID_TO_ITEM, WELCOME_IMAGES

# -------------------- ENV & Logging --------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # e.g. https://your-repl-url.repl.co/
PORT = int(os.getenv("PORT", "8000"))
RUN_WEB_ONLY = os.getenv("RUN_WEB_ONLY", "false").lower() in ("1", "true", "yes")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pizza-miniapp")

# -------------------- FastAPI app --------------------
app = FastAPI(title="Pizza Mini App Server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/api/menu")
async def get_menu():
    return JSONResponse({"menu": MENU, "promoCodes": PROMO_CODES})


def process_order_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = payload.get("items", [])
    address: str = payload.get("address", "")
    phone: str = payload.get("phone", "")
    payment: str = payload.get("payment", "cash")
    promo_code: str = (payload.get("promoCode") or "").strip().upper()

    total = 0.0
    lines: List[str] = []
    for it in items:
        item_id = int(it.get("id"))
        qty = max(1, int(it.get("qty", 1)))
        item = ITEM_ID_TO_ITEM.get(item_id)
        if not item:
            continue
        line_total = item["price"] * qty
        total += line_total
        lines.append(f"• {item['name']} × {qty} = {line_total}₽")

    discount_pct = PROMO_CODES.get(promo_code, 0)
    discount_amount = total * discount_pct / 100
    final_total = total - discount_amount

    order_id = int(datetime.now().timestamp())

    return {
        "orderId": order_id,
        "items": items,
        "lines": lines,
        "address": address,
        "phone": phone,
        "payment": payment,
        "promoCode": promo_code,
        "total": round(total, 2),
        "discountPct": discount_pct,
        "discountAmount": round(discount_amount, 2),
        "finalTotal": round(final_total, 2),
    }


@app.post("/api/order")
async def create_order(payload: Dict[str, Any]):
    if payload.get("type") != "order":
        return JSONResponse({"error": "invalid payload type"}, status_code=400)
    data = process_order_payload(payload)
    return JSONResponse(data)

# Serve static Mini App at root
app.mount("/", StaticFiles(directory="webapp", html=True), name="webapp")


# -------------------- Telegram bot --------------------
async def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set in .env")

    # Lazy imports so that web-only mode works without aiogram installed
    from aiogram import Bot, Dispatcher, Router, types, F
    from aiogram.enums import ParseMode
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    from aiogram.client.default import DefaultBotProperties

    def build_miniapp_keyboard() -> InlineKeyboardMarkup:
        if not WEBAPP_URL:
            raise RuntimeError("WEBAPP_URL is not set in .env")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🍕 Открыть Mini App", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        return kb

    router = Router()

    @router.message(F.text == "/start")
    async def on_start(message: types.Message):
        await message.answer_photo(
            photo=WELCOME_IMAGES[0],
            caption=(
                "🍕 Добро пожаловать!\n\n"
                "Откройте Mini App, чтобы выбрать пиццу и напитки, оформить заказ и оплатить."
            ),
            reply_markup=build_miniapp_keyboard(),
        )

    @router.message(F.web_app_data)
    async def webapp_data_handler(message: types.Message, bot: Bot):
        try:
            payload = json.loads(message.web_app_data.data)
        except Exception:
            await message.answer("Не удалось прочитать данные заказа.")
            return

        if payload.get("type") != "order":
            await message.answer("Получены данные неизвестного типа.")
            return

        data = process_order_payload(payload)

        user_text_parts = [
            f"✅ Заказ №{data['orderId']} оформлен!",
            "",
            "Состав:",
            *data["lines"],
            "",
            f"Сумма: {data['total']:.2f}₽",
        ]
        if data["discountPct"]:
            user_text_parts.append(
                f"Скидка {data['discountPct']}%: -{data['discountAmount']:.2f}₽"
            )
        user_text_parts.append(f"Итого к оплате: {data['finalTotal']:.2f}₽")
        user_text_parts.extend([
            "",
            f"Адрес: {data['address']}",
            f"Телефон: {data['phone']}",
            f"Оплата: {'Карта' if data['payment'] == 'card' else 'Наличные'}",
        ])

        await message.answer("\n".join(user_text_parts))

        if MANAGER_CHAT_ID:
            manager_text_parts = [
                f"🚨 НОВЫЙ ЗАКАЗ №{data['orderId']}",
                f"Клиент: {message.from_user.full_name} (@{message.from_user.username})",
                f"Телефон: {data['phone']}",
                f"Адрес: {data['address']}",
                f"Оплата: {'Карта' if data['payment'] == 'card' else 'Наличные'}",
                "",
                "Состав:",
                *data["lines"],
                "",
                f"Сумма: {data['total']:.2f}₽",
            ]
            if data["discountPct"]:
                manager_text_parts.append(
                    f"Скидка {data['discountPct']}%: -{data['discountAmount']:.2f}₽"
                )
            manager_text_parts.append(f"Итого: {data['finalTotal']:.2f}₽")
            try:
                await bot.send_message(chat_id=MANAGER_CHAT_ID, text="\n".join(manager_text_parts))
            except Exception as e:
                logger.error(f"Failed to notify manager: {e}")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot polling started")
    await dp.start_polling(bot)


async def run_web():
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    logger.info(f"Web server starting on 0.0.0.0:{PORT}")
    await server.serve()


async def main():
    web_task = asyncio.create_task(run_web())
    if RUN_WEB_ONLY or not BOT_TOKEN:
        await web_task
    else:
        await asyncio.gather(web_task, run_bot())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")