# -*- coding: utf-8 -*-
"""Bir martalik yordamchi: guruh va admin ID'larini olish uchun.

Asosiy bot (main.py) ishga tushishi uchun baza kerak, lekin BRON_GROUP_ID /
OPLATA_GROUP_ID / BOOTSTRAP_ADMIN_ID ni bazasiz, hatto shu qiymatlarni
bilmasdan ham olish kerak — shuning uchun alohida, DB'ga bog'liq bo'lmagan
skript.

Ishlatish:
    python get_ids.py

Keyin:
    - botni shaxsiy chatga /start yozing        -> o'zingizning ID'ingiz
    - botni BRON guruhiga admin qilib qo'shing, u yerda istalgan xabar yozing
      -> BRON_GROUP_ID
    - botni OPLATA guruhiga ham xuddi shunday qo'shing -> OPLATA_GROUP_ID

Ishni tugatgach shu faylni o'chirib tashlashingiz mumkin — asosiy botga
kerak emas.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit(".env da BOT_TOKEN yo'q")

dp = Dispatcher()


@dp.message()
async def echo_ids(message: Message):
    chat = message.chat
    user = message.from_user
    text = (
        f"💬 Chat ID: <code>{chat.id}</code>  (turi: {chat.type})\n"
        f"🏷 Chat nomi: {chat.title or chat.full_name or '-'}\n"
        f"🆔 Sizning ID: <code>{user.id}</code>\n"
        f"👤 {user.full_name}"
    )
    print("=" * 50)
    print(f"chat.id={chat.id}  chat.type={chat.type}  chat.title={chat.title}")
    print(f"user.id={user.id}  user.full_name={user.full_name}")
    print("=" * 50)
    await message.answer(text, parse_mode="HTML")


async def main() -> None:
    bot = Bot(token=TOKEN)
    me = await bot.get_me()
    logger.info("ID-yig'uvchi ishga tushdi: @%s. To'xtatish uchun Ctrl+C.", me.username)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
