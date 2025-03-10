import os
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from aiogram import types
from loader import dp

from keyboards.inline import menu   

from database.db import add_user, get_user_data, update_trial_plan_for_user, calculate_remaining_time, get_user_time_registration, is_trial_plan_active, get_user_row_number
from keyboards.reply import cmd_b
#from handlers.admin import admin_panel


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)  # Получаем данные пользователя
    
    if user_data:  
        await message.answer("Добро пожаловать в бот Meow Фриланс!\n\n"
                             "🚀 Найдите клиентов быстро, удобно и просто!\n\n"
                             "Для получения дополнительной информации напишите /help.\n\n"
                            "Для выхода в личный кабинет напишите /me")
        
        await message.answer("❕️ Нажмите /Vacancies, чтобы начать получать вакансии")
    else:
        add_user(user_id)  # Добавляем пользователя в БД
        await message.answer("Добро пожаловать! Вы зарегистрированы в системе.")

        await message.answer("Профессия «Веб-Дизайнер» выбрана успешно. Следуйте инструкции ниже")

        welcome_text = """
❕️ Нажмите /vacancies, чтобы начать получать вакансии\n❕️ Нажмите /info, чтобы начать получать вакансии"""

        await message.answer(welcome_text, reply_markup = cmd_b.admin())



# Обработчик команды /vacancies
@dp.message(Command("Vacancies"))
async def vacancies(message: types.Message):
    user_id = message.from_user.id
    get_user_row_number(user_id)  # Обновляем глобальную переменную перед использованием
    
    if is_trial_plan_active(user_id):

        await message.answer_photo(
            types.FSInputFile(path="src\\bot\\media\\botDescription.png"),
            caption=f"Подписка на вакансии активна. До окончания подписки осталось: {calculate_remaining_time(user_id)}"
        )

    else:

        await message.answer_photo(
            types.FSInputFile(path="src\\bot\\media\\botDescription.png"),
            caption="Подписка на вакансии закончилась"
        )

        await message.answer('➤ Нажмите /tarifs')
        
        # Обновляем триал-план в базе данных, если он еще не обновлен
        update_trial_plan_for_user(user_id)



@dp.message(Command("info"))
async def infor(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)  # Добавляем пользователя в БД, если его нет
    user_data = get_user_data(user_id)  # Получаем данные пользователя
    
    if user_data:
        response = "\n".join([f"📌 {key}: {value}" for key, value in user_data.items()])
    else:
        response = "❌ Ошибка: данные не найдены."

    await message.answer(f"✅ Личный кабинет:\n\n{response}")


@dp.message(Command("sudo"))
async def infor(message: types.Message):
    if message.from_user.id == int(os.getenv('adminID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=menu.defShowBotAdminMenu())
    else:
        await message.reply('Вы не являетесь админом.', reply_markup=menu.defShowBotUserMenu())


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text if message.text else 'А где текст?')



# for admin











    
