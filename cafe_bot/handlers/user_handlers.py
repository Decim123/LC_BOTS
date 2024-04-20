from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InputFile
from keyboards.keyboard import groups_kb, menu_profile_kb, create_products_kb, create_day_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import save_username_to_database
from aiogram import types
from services.services import available_products_and__groups, get_product_names_by_group, get_products, day_list, add_choise, delete_choise, add_order, get_choises_by_id, next_day_of_week

av_products_ids, av_groups = available_products_and__groups()
products = get_products()
week_days = day_list()

router = Router()

user_state = {}

async def process_default_message(message: Message):
    await message.answer(text=LEXICON_RU['not_supported_answer'], reply_markup=menu_profile_kb)

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=menu_profile_kb)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=menu_profile_kb)


@router.message(F.text == LEXICON_RU['menu_button'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['make_a_choise'], reply_markup=groups_kb)

@router.message(F.text == 'Назад')
async def process_back_answer(message: Message):
    await message.answer(text=LEXICON_RU['make_a_choise'], reply_markup=groups_kb)

@router.message(F.text == 'Отмена')
async def process_cancel_answer(message: Message):
    tg_id = message.from_user.id
    delete_choise(tg_id)
    await message.answer(text='Отмена \n\n <b>Заказать что-то другое?</b>', reply_markup=menu_profile_kb)

@router.message(F.text == LEXICON_RU['profile_button'])
async def process_profile_button(message: Message):
    tg_id = message.from_user.id
    user_state[tg_id] = 'waiting_for_username'
    await message.answer(text=LEXICON_RU['name_pls'])


for word in av_groups:
    @router.message(F.text == word)
    async def process_group_word(message: Message, word=word):
        products_kb, av_products_names_in_group = create_products_kb(word)
        await message.answer(text=word, reply_markup=products_kb)

for key in products:
    @router.message(F.text == key)
    async def products_card(message: Message, key=key):
        product_info = products.get(key)
        product_photo = product_info.get('image')
        product_price = product_info.get('price')
        day_kb = create_day_kb()
        tg_id = message.from_user.id
        add_choise(tg_id, key)
        await message.answer_photo(photo=types.FSInputFile('cafe_app/static/img/' + product_photo))
        await message.answer(text='Цена:' + str(product_price) + '\n\nУчтите что предзаказ на завтра доступен только до 14:00 сегодняшнего дня ' + '\n\n<b>Выберите дату:</b>', reply_markup=day_kb)
        
for day in week_days:
    @router.message(F.text == day)
    async def process_group_word(message: Message, day=day):
        tg_id = message.from_user.id
        choised_product = get_choises_by_id(tg_id)
        data = next_day_of_week(day)
        add_order(tg_id, choised_product, day, data)
        delete_choise(tg_id)
        await message.answer(text='Отлично, ваш предзаказ создан! \n\n <b>Заказать еще?</b>', reply_markup=menu_profile_kb)

@router.message()
async def process_user_input(message: Message):
    tg_id = message.from_user.id
    if tg_id in user_state and user_state[tg_id] == 'waiting_for_username':
        username = message.text
        save_username_to_database(tg_id, username)
        await message.answer(text=LEXICON_RU['change_name'], reply_markup=menu_profile_kb)
        del user_state[tg_id]
    else:
        await process_default_message(message)