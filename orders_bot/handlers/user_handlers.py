from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboard import create_day_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import delete_orders_by_date, days_of_week, get_orders_by_time
from datetime import datetime

day_kb = create_day_kb()
current_date = datetime.now().strftime('%Y-%m-%d')

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    
    await message.answer(text=LEXICON_RU['/start'], reply_markup=day_kb)

for day in days_of_week:
    @router.message(F.text == day)
    async def process_group_word(message: Message, day=day):
        delete_orders_by_date(current_date)
        try: 
            orders = get_orders_by_time(day)
            await message.answer(text=str(orders), reply_markup=day_kb)
        except:
            await message.answer(text="Нет заказов на этот день", reply_markup=day_kb)



