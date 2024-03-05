import logging
import asyncio
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
# Бот
bot = Bot(token="7093707672:AAFr5N3UN87FJxsMSm_oh81WKXIS4flY9Rg")

# Диспетчер
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Хэндлер на команду /test1
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Вариант1")
    buttons = ["Вариант1", "Вариант2"]
    keyboard.add(*buttons)
    await message.answer("Выберите вариант", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Вариант1")
async def var1(message: types.Message):
    await message.reply("Ответ1")

@dp.message_handler(lambda message: message.text == "Вариант2")
async def var2(message: types.Message):
    await message.reply("Ответ2")

@dp.message_handler(commands="inline_url")
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="GitHub", url="https://github.com"),
        types.InlineKeyboardButton(text="Help PtSecurity", url="https://help.ptsecurity.com")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Кнопки-ссылки", reply_markup=keyboard)

@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1,10)))
    await call.answer(text="Спасибо, что воспользовались ботом!", show_alert=True)

user_data = {}

def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
        types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard())

@dp.message_handler(commands="numbers")
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())

@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)

    action = call.data.split("_")[1]
    if action == "incr":
        user_data[call.from_user.id] = user_value+1
        await update_num_text(call.message, user_value+1)
    elif action == "decr":
        user_data[call.from_user.id] = user_value-1
        await update_num_text(call.message, user_value-1)
    elif action == "finish":
        await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()

@dp.message_handler(commands="stop")
async def cmd_ping2(message: types.Message):
    await message.reply("Спим...")

@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)
    await message.reply("Вы заблокированы")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True

if __name__=="__main__":
    executor.start_polling(dp,  skip_updates=True)
