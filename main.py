from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from handlers import user, worker
from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(user.router, worker.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())