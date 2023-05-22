from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import logging
import requests



TOKEN = config("TOKEN")

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start", "anime"])
async def start(message: types.Message):
    await message.answer(f"Salam {message.from_user.full_name}")


@dp.message_handler(commands=["quiz"])
async def quiz_1(message: types.Message):
    marcap = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Next", callback_data="button")
    marcap.add(button)
    question = "Кто является главной героиней в аниме 'Sailor Moon'"
    answers = [
        "Sakura Kinomoto",
        "Bulma Briefs",
        "Usagi Tsukino",
        "Misato Katsuragi",
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type="quiz",
        correct_option_id=2,
        open_period=15,
        reply_markup=marcap
    )
@dp.callback_query_handler(text="button")
async def quiz_2(call: types.CallbackQuery):
    question = "В каком аниме главный герой является пиратом и путешествует по Grand Line в поисках One Piece?"
    answers = [
        " Naruto",
        "Attack on Titan",
        "One Piece",
        "Dragon Ball Z",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type="quiz",
        correct_option_id=2,
        open_period=15,
        
    )



@dp.message_handler(commands=["mem"])
async def mem_command_handler(message:types.Message):
    response = requests.get("https://picsum.photos/200/300")  # Замените размер изображения по вашему усмотрению
    if response.status_code == 200:
        image_url = response.url
        # Отправка изображения в ответе на команду "mem"
        await bot.send_photo(message.chat.id, image_url)
    else:
        await message.answer("Произошла ошибка при получении изображения.")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def number_handler(message: types.Message):
    try:
        number = int(message.text)
        squared = number ** 2
        await message.answer(f"Квадрат числа {number} равен {squared}")
    except ValueError:
        await bot.send_message(message.from_user.id, message.text)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
