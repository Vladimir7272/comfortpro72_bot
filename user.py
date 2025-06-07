from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.menu import main_menu

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Это ComfortPro — сервис по обслуживанию кондиционеров и вентиляции в Тюмени.",
        reply_markup=main_menu()
    )

@router.message(F.text == "Вызвать мастера")
async def request_service(message: Message):
    await message.answer("📍 Введите адрес, куда нужно вызвать мастера:")