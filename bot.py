from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio, os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(msg: Message):
    await msg.answer("🚗 Бот подбора дисков и шин запущен")

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(start, Command("start"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
