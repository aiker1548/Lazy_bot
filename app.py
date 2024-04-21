import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from aiogram.utils import executor
import pyautogui
from audio_control import decrease_volume, increase_volume

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
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Прибавить звук на сервере на 5%", callback_data='increase_volume'),
        InlineKeyboardButton("Убавить звук на сервере на 5%", callback_data='decrease_volume'),
        InlineKeyboardButton("Выключить компьютер", callback_data='shutdown_computer'),
        InlineKeyboardButton("Это второй mp3", callback_data='eto_vtoroy'),
        InlineKeyboardButton("Play/Stop", callback_data='play_stop'),
        InlineKeyboardButton("Управление мышью", callback_data='mouse_control_menu'),
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
        await increase_volume()
        await bot.answer_callback_query(callback_query.id, text="Звук увеличен на 5%")
    elif action == 'decrease_volume':
        await decrease_volume()
        await bot.answer_callback_query(callback_query.id, text="Звук уменьшен на 5%")
    elif action == 'shutdown_computer':
        if callback_query.from_user.id == DIMAS_ID:
            await bot.send_message(callback_query.from_user.id, text="Ты че реально думал, что я дам тебе право мне комп вырубить, тупой качок")
        elif callback_query.from_user.id == ADMIN_ID:
            # Ваш код для выключения компьютера
            await bot.answer_callback_query(callback_query.id, text="Компьютер выключен")
    elif action == 'play_stop':
        pyautogui.press('space')
        await bot.answer_callback_query(callback_query.id, text="Кнопка нажата")
    elif action == 'mouse_control_menu':
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton("Поднять мышь", callback_data='move_mouse_up'),
            InlineKeyboardButton("Опустить мышь", callback_data='move_mouse_down'),
            InlineKeyboardButton("Клик мыши", callback_data='mouse_click'),
            InlineKeyboardButton("Назад", callback_data='back_to_main_menu'),
        ]
        keyboard.add(*buttons)
        await bot.send_message(callback_query.from_user.id, "Управление мышью:", reply_markup=keyboard)
    elif action == 'move_mouse_up':
        pyautogui.move(0, -10)  # Двигаем курсор мыши вверх
        await bot.answer_callback_query(callback_query.id, text="Курсор мыши поднят")
    elif action == 'move_mouse_down':
        pyautogui.move(0, 10)  # Двигаем курсор мыши вниз
        await bot.answer_callback_query(callback_query.id, text="Курсор мыши опущен")
    elif action == 'mouse_click':
        pyautogui.click()  # Кликаем кнопку мыши
        await bot.answer_callback_query(callback_query.id, text="Кнопка мыши нажата")
    elif action == 'back_to_main_menu':
        await bot.edit_message_text("Привет! Выбери действие:", inline_message_id=callback_query.inline_message_id, reply_markup=None)

# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
