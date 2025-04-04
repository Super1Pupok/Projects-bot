from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Ученик'
        ),
        KeyboardButton(
            text='Наставник'
        )
    ]
], resize_keyboard=True)