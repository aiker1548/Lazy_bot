import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from aiogram.utils import executor
from audio_control import increase_volume, decrease_volume
import pyautogui


# Включаем логгирование
logging.basicConfig(level=logging.INFO)


# Создаем объект бота
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

# Обработчик команды /start
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id not in [ADMIN_ID, DIMAS_ID]:
        await message.answer("Вы не админ или Димас!")
        return
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Прибавить звук на сервере на 5%", callback_data='increase_volume'),
        InlineKeyboardButton("Убавить звук на сервере на 5%", callback_data='decrease_volume'),
        InlineKeyboardButton("Выключить компьютер", callback_data='shutdown_computer'),
        InlineKeyboardButton("Это второй mp3", callback_data='eto_vtoroy'),
        InlineKeyboardButton("Play/Stop", callback_data='play_stop'),
    ]
    keyboard.add(*buttons)
    await message.answer("Привет! Выбери действие:", reply_markup=keyboard)

# Обработчик нажатия на кнопки
@dispatcher.callback_query_handler(lambda c: True)
async def inline_buttons_handler(callback_query: types.CallbackQuery):
    action = callback_query.data
    if callback_query.from_user.id not in [ADMIN_ID, DIMAS_ID]:
        await bot.answer_callback_query(callback_query.id, text="Вы не админ или Димас!")
        return
    if action == 'increase_volume':
        increase_volume()
        await bot.answer_callback_query(callback_query.id, text="Звук увеличен на 5%")
    elif action == 'decrease_volume':
        decrease_volume()
        await bot.answer_callback_query(callback_query.id, text="Звук уменьшен на 5%")
    elif action == 'shutdown_computer':
        if callback_query.from_user.id == DIMAS_ID:
            await bot.answer_callback_query(callback_query.id, text="Ты че реально думал, что я дам тебе право мне комп вырубить, тупой качок")
        elif callback_query.from_user.id == ADMIN_ID:
            # Ваш код для выключения компьютера
            await bot.answer_callback_query(callback_query.id, text="Компьютер выключен")
    elif action == 'play_stop':
        pyautogui.press('space')
        await bot.answer_callback_query(callback_query.id, text="Кнопка нажата")
    #elif action == 'eto_vtoroy':


  
# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
