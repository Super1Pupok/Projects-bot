import asyncio
import logging
import sqlite3
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from uchenik import ureply_keyboard
from nastavnik import nreply_keyboard
from fms_classes import classes_keyboard
from role import role_keyboard
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message


class Signup(StatesGroup):
    name = State()
    second_name = State()
    role = State()
    fms_class = State()
    project = State()


TOKEN = '7604395608:AAFgTgPy5GrkeWFI8aJYOZ1rBwZ9I8E27E4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

connection = sqlite3.connect('nnn.db')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Пользователи (
user_id INT PRIMARY KEY, 
name TEXT, 
second_name TEXT, 
role TEXT, 
fms_class TEXT, 
project TEXT)""")
connection.commit()


def user_exists(user_id):
    with connection:
        result = cursor.execute("SELECT * FROM  Пользователи WHERE user_id = ?", (user_id,)).fetchall()
        return bool(len(result))


def check_role(user_id):
    with connection:
        return str(cursor.execute("SELECT role FROM  Пользователи WHERE user_id = ?", (user_id,)).fetchall())


@dp.message(CommandStart())
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, '''Здравствуй! Это бот для проверки проектов!
          Для начала работы необходима регистрация. Введи команду /register''')


@dp.message(Command('register'))
async def command_register_handler(message: Message, state: FSMContext) -> None:
    if not user_exists(message.from_user.id):
        await message.answer('Для начала введи своё полное имя')
        await state.set_state(Signup.name)
    else:
        if check_role(message.from_user.id) == "[('Ученик',)]":
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!', reply_markup=ureply_keyboard)
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!', reply_markup=nreply_keyboard)


@dp.message(Signup.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Signup.second_name)
    await message.answer('Теперь введи свою фамилию')


@dp.message(Signup.second_name)
async def process_second_name(message: Message, state: FSMContext) -> None:
    await state.update_data(second_name=message.text)
    await state.set_state(Signup.role)
    await message.answer('Теперь выбери роль', reply_markup=role_keyboard)


@dp.message(Signup.role)
async def process_role(message: Message, state: FSMContext) -> None:
    if message.text == 'Ученик':
        await state.update_data(role=message.text)
        await state.set_state(Signup.fms_class)
        await message.answer('Теперь выбери свой класс', reply_markup=classes_keyboard)
    elif message.text == 'Наставник':
        await state.update_data(role=message.text)
        await state.update_data(fms_class=None)
        await state.update_data(project=None)
        current_state = await state.get_data()
        await state.clear()
        await process_succes(message.from_user.id, current_state)
    else:
        await bot.send_message(message.from_user.id, 'Кажется, я тебя не понимаю. Выбери свою роль')
        await state.set_state(Signup.role)


@dp.message(Signup.fms_class)
async def process_fms_class(message: Message, state: FSMContext) -> None:
    if message.text == 'Μ(Мю)' or message.text == 'Ξ(Кси)' or message.text == 'Ο(Омикрон)' or message.text == 'Π(Пи)' or message.text == 'Ρ(Ро)' or message.text == 'Σ(Сигма)' or message.text == 'Τ(Тау)' or message.text == 'Φ(Фи)' or message.text == 'Χ(Хи)' or message.text == 'Ψ(Пси)':
        await state.update_data(fms_class=message.text)
        await state.set_state(Signup.project)
        await message.answer('Укажи название своего проекта')
    else:
        await bot.send_message(message.from_user.id, 'Кажется, я тебя не понимаю. Выбери свой класс')
        await state.set_state(Signup.fms_class)


@dp.message(Signup.project)
async def process_project(message: Message, state: FSMContext) -> None:
    project = message.text
    await state.update_data(project=project)
    current_state = await state.get_data()
    await state.clear()
    await process_succes(message.from_user.id, current_state)


async def process_succes(user_id, current_state):
    with connection:
        cursor.execute(
            "INSERT INTO 'Пользователи' ('user_id', 'name', 'second_name', 'role', 'fms_class', 'project') VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, current_state['name'], current_state['second_name'], current_state['role'],
             current_state['fms_class'], current_state['project']))
        connection.commit()
        if check_role(user_id) == "[('Ученик',)]":
            reply_keyboard = ureply_keyboard
        else:
            reply_keyboard = nreply_keyboard
        await bot.send_message(user_id, f'Регистрация прошла успешно!', reply_markup=reply_keyboard)


@dp.message()
async def bot_message(message: types.Message):
    if message.text == 'Сдать работу' and check_role(message.from_user.id) == 'Ученик':
        pass
    elif message.text == 'Посмотреть список учеников' and check_role(message.from_user.id) == 'Наставник':
        pass
    else:
        await bot.send_message(message.from_user.id, 'Кажется я вас не понимаю 🤔')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
