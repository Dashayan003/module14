from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton(text="Рассчитать")
button_info = types.KeyboardButton(text="Информация")
button_buy = types.KeyboardButton(text="Купить")
keyboard.add(button_calculate, button_info, button_buy)


inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
inline_buttons = [
    types.InlineKeyboardButton(text=f"Product{i+1}", callback_data="product_buying")
    for i in range(4)
]
inline_keyboard.add(*inline_buttons)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью. Выберите действие:",
        reply_markup=keyboard
    )


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Рассчитать'])
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories} ккал.")

    await state.finish()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    products = [
        {"name": "Product1", "description": "Описание 1", "price": 100, "image": "product1.jpg"},
        {"name": "Product2", "description": "Описание 2", "price": 200, "image": "product2.jpg"},
        {"name": "Product3", "description": "Описание 3", "price": 300, "image": "product3.jpg"},
        {"name": "Product4", "description": "Описание 4", "price": 400, "image": "product4.jpg"},
    ]

    for product in products:
        await message.answer_photo(
            photo=open(product["image"], 'rb'),
            caption=f"Название: {product['name']} | Описание: {product['description']} | Цена: {product['price']} руб."
        )

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
