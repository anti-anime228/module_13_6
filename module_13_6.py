from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton(text='Информация')
button_calculate = KeyboardButton(text='Рассчитать')
kb.add(button_info)
kb.add(button_calculate)

kb_line = InlineKeyboardMarkup()

button_line1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_line2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb_line.add(button_line1)
kb_line.add(button_line2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Чем могу помочь?", reply_markup=kb)


@dp.message_handler(text='Рассчитать')  # commands
async def main_menu(message):
    await message.answer("Выбери опцию", reply_markup=kb_line)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    formula = ('Формула для мужчин:\n10 * Вес + 6,25 * Рост – 5 * Возраст + 5'
               '\nФормула для женщин:\n10 * Вес + 6,25 * Рост – 5 * Возраст – 161')
    await call.message.answer(formula)
    await call.answer()


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Этот бот поможет расчитать норму калорий в день')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
