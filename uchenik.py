from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ureply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сдать работу'
        )
    ]
], resize_keyboard=True)