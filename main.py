import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

router = Router()

def get_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вызвать мастера")],
            [KeyboardButton(text="Оформить подписку")],
            [KeyboardButton(text="Я мастер")]
        ],
        resize_keyboard=True
    )
    return kb

@router.message(Command("start"))
async def start_cmd(msg: Message):
    await msg.answer("Привет! Я бот ComfortPro. Что нужно?", reply_markup=get_menu())

@router.message(Text("Вызвать мастера"))
async def request_service(msg: Message):
    await msg.answer("📍 Введите адрес, куда нужно вызвать мастера:")

@router.message(Text("Я мастер"))
async def master_reg(msg: Message):
    await msg.answer("👷 Введите свои ФИО, город и опыт. Мы свяжемся с вами.")

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())