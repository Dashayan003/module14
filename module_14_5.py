from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import crud_functions
from crud_functions import initiate_db, add_user, is_included
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton(text="Рассчитать")
button_info = types.KeyboardButton(text="Информация")
button_buy = types.KeyboardButton(text="Купить")
button_signup = types.KeyboardButton(text="Регистрация")
keyboard.add(button_calculate, button_info, button_buy, button_signup)


inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
inline_buttons = [
    types.InlineKeyboardButton(text=f"Product{i+1}", callback_data="product_buying")
    for i in range(4)
]
inline_keyboard.add(*inline_buttons)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State() 


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        "Привет! Я бот, помогающий твоему здоровью. Выберите действие:",
        reply_markup=keyboard
    )


@dp.message_handler(text=["Регистрация"])
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя.")
        return
    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    age = message.text
    await state.update_data(age=age)

    data = await state.get_data()
    username = data["username"]
    email = data["email"]
    age = data["age"]
    balance = 1000  

    add_user(username, email, age, balance)

    await message.answer(f"Вы успешно зарегистрированы!\nИмя пользователя: {username}\nEmail: {email}\nВозраст: {age}")

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
