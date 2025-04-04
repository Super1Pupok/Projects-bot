from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

classes_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Μ(Мю)'
        ),
        KeyboardButton(
            text='Ξ(Кси)'
        ),
        KeyboardButton(
            text='Ο(Омикрон)'
        )
    ],
    [
        KeyboardButton(
            text='Π(Пи)'
        ),
        KeyboardButton(
            text='Ρ(Ро)'
        ),
        KeyboardButton(
            text='Σ(Сигма)'
        )
    ],
    [
        KeyboardButton(
            text='Τ(Тау)'
        ),
        KeyboardButton(
            text='Φ(Фи)'
        ),
        KeyboardButton(
            text='Χ(Хи)'
        ),
        KeyboardButton(
            text='Ψ(Пси)'
        )
    ]
], resize_keyboard=True)
