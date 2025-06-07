from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    buttons = [
        [KeyboardButton(text="Вызвать мастера")],
        [KeyboardButton(text="Оформить подписку")],
        [KeyboardButton(text="Я мастер")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)