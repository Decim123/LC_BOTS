from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from services.services import day_list

def create_day_kb():
    days = day_list()
    day_buttons = []
    day_row = []
    for index, day in enumerate(days):
        button = KeyboardButton(text=day)
        day_row.append(button)
        if (index + 1) % 3 == 0 or index == len(days) - 1:
            day_buttons.append(day_row)
            day_row = []

    # Создание клавиатуры
    day_kb = ReplyKeyboardMarkup(keyboard=day_buttons, resize_keyboard=True)
    return day_kb