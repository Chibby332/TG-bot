from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import string

import app.keyboards as kb 

router = Router()

class InfoRecipient(StatesGroup):
    SNILS = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Здравствуйте. Если вы хотите узнать информацию о своей завявке, нажмите кнопки в меню.', reply_markup=kb.main)

@router.message(F.text == ('Помощь'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи.', reply_markup=kb.cancel)

@router.message(F.text == ('Узнать информацию о заявке'))
async def info(message: Message, state: FSMContext):
    await state.set_state(InfoRecipient.SNILS)
    await message.answer('Введите номер вашего СНИЛСа', reply_markup=kb.cancel)

@router.message(InfoRecipient.SNILS)
async def info_snils(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer('Возвращаемся в главое меню.', reply_markup=kb.main)
    elif message.text.isdigit() == False:
        await message.answer('Некорректный ввод. Введите номер СИНЛСа')
    else:
        await state.update_data(SNILS=message.text)
        data = await state.get_data()
        await message.answer(f'Ваш снилс: {data["SNILS"]}')

@router.message(F.text == ('Отмена'))
async def cancel(message: Message):
    await message.answer('Возвращаемся в главое меню.', reply_markup=kb.main)