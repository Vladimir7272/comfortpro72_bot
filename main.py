from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import os

from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

router = Router()

def main_menu():
    buttons = [
        [KeyboardButton(text="Вызвать мастера")],
        [KeyboardButton(text="Оформить подписку")],
        [KeyboardButton(text="Я мастер")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Это ComfortPro — сервис по обслуживанию кондиционеров и вентиляции в Тюмени.",
        reply_markup=main_menu()
    )

@router.message(Text("Вызвать мастера"))
async def request_service(message: Message):
    await message.answer("📍 Введите адрес, куда нужно вызвать мастера:")

@router.message(Text("Я мастер"))
async def master_form(message: Message):
    await message.answer("👷 Введите ваши ФИО, опыт работы и город. Мы свяжемся с вами после проверки.")

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())