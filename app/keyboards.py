from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Узнать список заявок по СНИЛСУ')],
                                     [KeyboardButton(text='Узнать информацию о заявке')],
                                     [KeyboardButton(text='Помощь')],
                                     ],
                                      resize_keyboard=True,
                                      input_field_placeholder='Выберите пункт меню...')

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                                      resize_keyboard=True,
                                      input_field_placeholder='Выберите пункт меню...')
