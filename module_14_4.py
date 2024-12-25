from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud_functions import initiate_db, get_all_products
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
    products = get_all_products()

    for product in products:
        product_id, title, description, price, image_path = product
        text = f"Название: {title} | Описание: {description} | Цена: {price} руб."

        if image_path:
            try:
                with open(image_path, 'rb') as image_file:
                    await message.answer_photo(photo=image_file, caption=text)
            except FileNotFoundError:
                await message.answer(text)

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)
