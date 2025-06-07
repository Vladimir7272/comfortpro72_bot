import asyncio
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

router = Router()

class OrderForm(StatesGroup):
    waiting_for_city = State()
    waiting_for_address = State()
    waiting_for_phone = State()

def get_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛠 Вызвать мастера")],
            [KeyboardButton(text="📅 Оформить подписку")],
            [KeyboardButton(text="👷 Я мастер")]
        ],
        resize_keyboard=True
    )
    return kb

@router.message(Command("start"))
async def start_cmd(msg: Message):
    await msg.answer("👋 Привет! Я бот ComfortPro — помогу с кондиционерами, вентиляцией и комфортом в доме.", reply_markup=get_menu())

@router.message(lambda msg: msg.text == "🛠 Вызвать мастера")
async def request_service_start(msg: Message, state: FSMContext):
    await msg.answer("🏙️ Введите ваш город:")
    await state.set_state(OrderForm.waiting_for_city)

@router.message(OrderForm.waiting_for_city)
async def request_service_city(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await msg.answer("📍 Введите адрес, куда вызвать мастера:")
    await state.set_state(OrderForm.waiting_for_address)

@router.message(OrderForm.waiting_for_address)
async def request_service_address(msg: Message, state: FSMContext):
    await state.update_data(address=msg.text)
    await msg.answer("📞 Введите контактный телефон:")
    await state.set_state(OrderForm.waiting_for_phone)

@router.message(OrderForm.waiting_for_phone)
async def request_service_phone(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    city = data.get("city")
    address = data.get("address")
    phone = msg.text
    user = msg.from_user

    await msg.answer("✅ Спасибо! Заявка принята. Мы скоро свяжемся с вами.")

    admin_message = (
        f"📬 Новая заявка на выезд:\n"
        f"Город: {city}\n"
        f"Адрес: {address}\n"
        f"Телефон: {phone}\n"
        f"Имя: {user.full_name}\n"
        f"ID: {user.id}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    await state.clear()

@router.message(lambda msg: msg.text == "👷 Я мастер")
async def master_form(msg: Message):
    await msg.answer("👷 Введите, пожалуйста, в одном сообщении:\n1. Ваше ФИО\n2. Город\n3. Опыт работы (в годах)\n4. Контактный телефон")

@router.message(lambda msg: msg.text and all(keyword in msg.text.lower() for keyword in ["г", "т", "ф"]))
async def save_master_info(msg: Message, bot: Bot):
    user = msg.from_user
    await msg.answer("✅ Спасибо! Мы свяжемся с вами после проверки.")
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔧 Новый кандидат в мастера:\n{msg.text}\n@{user.username or 'без username'}\nID: {user.id}"
    )

@router.message(lambda msg: msg.text == "📅 Оформить подписку")
async def subscribe_request(msg: Message):
    await msg.answer("📦 Напишите, пожалуйста:\n1. Модель кондиционера\n2. Адрес\n3. Контактный телефон")

@router.message(lambda msg: msg.text and any(x in msg.text.lower() for x in ["модель", "адрес", "тел"]))
async def save_subscription(msg: Message, bot: Bot):
    user = msg.from_user
    await msg.answer("✅ Подписка оформлена. Мы напомним об обслуживании через 6 месяцев.")
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📅 Новая подписка:\n{msg.text}\n@{user.username or 'без username'}\nID: {user.id}"
    )

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())