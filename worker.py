from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text

router = Router()

@router.message(Text("Я мастер"))
async def master_form(message: Message):
    await message.answer("👷 Введите ваши ФИО, опыт работы и город. Мы свяжемся с вами после проверки.")