from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU
from services.services import available_products_and__groups, get_product_names_by_ids, get_product_names_by_group, day_list

av_products_ids, av_groups = available_products_and__groups()
av_products_names = get_product_names_by_ids(av_products_ids)

button_yes = KeyboardButton(text=LEXICON_RU['menu_button'])
button_no = KeyboardButton(text=LEXICON_RU['profile_button'])


menu_profile_kb_builder = ReplyKeyboardBuilder()

menu_profile_kb_builder.row(button_yes, button_no, width=2)

menu_profile_kb: ReplyKeyboardMarkup = menu_profile_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

# ------- клавиатура для групп -------

buttons = []
row = []
for index, group in enumerate(av_groups):
    button = KeyboardButton(text=group)
    row.append(button)
    if (index + 1) % 3 == 0 or index == len(av_groups) - 1:
        buttons.append(row)
        row = []

# Создание клавиатуры
groups_kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# ------- клавиатура для товаров -------
def create_products_kb(group_name):
    product_names = get_product_names_by_group(group_name)
    av_products_names = get_product_names_by_ids(av_products_ids)
    av_products_names_in_group = [name for name in product_names if name in av_products_names]
    av_products_names_in_group.append('Назад')
    products_buttons = []
    products_row = []
    
    for index, product in enumerate(av_products_names_in_group):
        products_button = KeyboardButton(text=product)
        products_row.append(products_button)
        if (index + 1) % 3 == 0 or index == len(av_products_names_in_group) - 1:
            products_buttons.append(products_row)
            products_row = []

    # Создание клавиатуры
    products_kb = ReplyKeyboardMarkup(keyboard=products_buttons, resize_keyboard=True)
    return products_kb, av_products_names_in_group

# ------- клавиатура для дней -------

def create_day_kb():
    days = day_list()
    days.append('Отмена')
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