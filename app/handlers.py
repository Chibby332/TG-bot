from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import string

import app.keyboards as kb 
import app.database.requests as rq

router = Router()

class InfoRecipient(StatesGroup):
    SNILS = State()
    ID = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Здравствуйте. Если вы хотите узнать информацию о своей завявке, нажмите кнопки в меню.', reply_markup=kb.main)

@router.message(F.text == ('Помощь'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи.', reply_markup=kb.cancel)

@router.message(F.text == ('Узнать список заявок по СНИЛСУ'))
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
        requests = await rq.check_snils(message.text)
        
        if not requests:
            await message.answer('Такого SNILS нету')
        else:
            await state.update_data(SNILS=message.text)
            data = await state.get_data()

            await message.answer(f'Ваш СНИЛС: {data["SNILS"]}')
            requests_text = "\n".join([f"Заявка №{req_id} - {req_name}" for req_id, req_name in requests]) 
            await message.answer(f'Ваши заявки:\n{requests_text}')

@router.message(F.text == ('Узнать информацию о заявке'))
async def info(message: Message, state: FSMContext):
    await state.set_state(InfoRecipient.ID)
    await message.answer('Введите номер вашей заявки', reply_markup=kb.cancel)

@router.message(InfoRecipient.ID)
async def info_id(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer('Возвращаемся в главое меню.', reply_markup=kb.main)
    elif message.text.isdigit() == False:
        await message.answer('Некорректный ввод. Введите номер заявки')
    else:
        request_info = await rq.check_id(message.text)
        
        if not request_info:
            await message.answer('Заявки с таким номером нет')
        else:
            await state.update_data(ID=message.text)
            data = await state.get_data()

            await message.answer(
                f"Информация по заявке (номер заявки {data["ID"]}): "
                f"{request_info['request_name']} на сумму {request_info['money']} рублей. Статус: {request_info['status']}"
            )

@router.message(F.text == ('Отмена'))
async def cancel(message: Message):
    await message.answer('Возвращаемся в главое меню.', reply_markup=kb.main)