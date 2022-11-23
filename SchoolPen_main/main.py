import logging
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from settings import API_TOKEN

# Configure logging

logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет, я чат-бот! Нажми кнопку")
    logging.info(f"Message from {message.from_user.username}: {message.text}, {time.asctime()}")


@dp.message_handler(text='Часы работы')
async def buttons(message: types.Message):
    await message.answer(f"режим работы доставки:\n"
                         f"Ежедневно с 10-00 до 23-00\n"
                         f"Без перерыва и выходных\n"
                         f"Заказы принимаются с 10-00 до 22-00")


@dp.message_handler(text='Акции')
async def buttons(message: types.Message):
    await message.answer(f"При единовременном заказе на сумму \n"
                         f"от 2000 руб мы добавим в Ваш заказ\n"
                         f" приятный бонус от шеф-повара.")

@dp.message_handler(text='Доставка')
async def buttons(message: types.Message):
    await message.answer(f"Доставка осуществляется с 10-00 до\n"
                         f" 23-00 ежедневно, без перерывов и выходных.\n"
                         f"При заказе от 1500 руб. доставка осуществляется\n"
                         f" БЕСПЛАТНО в любую точку города.\n"
                         f"Среднее время доставки 30 мин с момента готовности заказа")

@dp.message_handler(text='Поднять настроение')
async def buttons(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Кошки", callback_data="cat"),
               InlineKeyboardButton("Собаки", callback_data="dog"),
               )

    await message.answer(f"Сегодня слишком хороший день чтобы грустить!", reply_markup=markup)


@dp.callback_query_handler(text_startswith="cat")
async def fun_handler(call: types.CallbackQuery):
    with open('data/cats.jpg', 'rb') as photo:
        await call.message.reply_photo(photo, caption='Без кота жизнь не та 😺 ')

    await call.answer()

@dp.callback_query_handler(text_startswith="dog")
async def fun_handler(call: types.CallbackQuery):
    with open('data/dogs.png','rb') as photo:
        await call.message.reply_photo(photo, caption="Собака-улыбака")

    await call.answer()

@dp.message_handler()
async def echo(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Поднять настроение", "Акции")
    markup.add("Часы работы", "Доставка")


    await message.answer(message.text, reply_markup=markup)
    logging.info(f"Message from {message.from_user.username}: {message.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
