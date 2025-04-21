import os
from aiogram.filters import Command, CommandStart

from aiogram.types import Message

from aiogram import types, F
from aiogram.types import CallbackQuery

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from loader import dp, bot

from keyboards.inline import menu   

from database.db import add_user, get_user_data, update_trial_plan_for_user, calculate_remaining_time, get_user_time_registration, is_trial_plan_active, get_user_row_number, setSubFor_3_days, setSubFor_7_days, setSubFor_30_days, setSubFor_365_days
#from keyboards.reply import cmd_b
#from handlers.admin import admin_panel

# Определяем группу состояний
class SubscriptionStates(StatesGroup):
    waiting_for_subscription = State()



@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)  # Получаем данные пользователя
    
    if user_data:  

        await message.answer("Добро пожаловать в бот Meow Фриланс!😻\n\n"
                             "🚀 Найдите клиентов быстро, удобно и просто!\n\n"
                             "Для получения дополнительной информации напишите /help.\n\n"
                            "Для выхода в личный кабинет напишите /me\n\n" \
                            "/sudo - админ панель (требуются права)")
        
        await message.answer("❕️ Нажмите /Vacancies, чтобы начать получать вакансии")

        await message.answer_photo(
types.FSInputFile(path="src\\bot\\media\\botDescription.png"),
caption=f"⏳ Оставшееся время действия Вашей подписки: \n{calculate_remaining_time(user_id)}"
)
    else:
        add_user(user_id)  # Добавляем пользователя в БД
        await message.answer("Добро пожаловать в бот Meow Фриланс!😻\nВы зарегистрированы в системе.")

        await message.answer("🚀 Найдите клиентов быстро, удобно и просто!\n\n"
                             "Для получения дополнительной информации напишите /help.\n\n"
                            "Для выхода в личный кабинет напишите /me")
        
        await message.answer_photo(
types.FSInputFile(path="src\\bot\\media\\botDescription.png"),
caption=f"⏳ Оставшееся время действия Вашей подписки: \n{calculate_remaining_time(user_id)}"
)
        

        
@dp.message(Command("help"))
async def start(message: Message):
    await message.answer("Список команд:\n\n"
                             "/start - начать\n\n"
                             "/me - личный кабинет\n\n"
                             "/Vacancies - команда для получения вакансий\n\n"
                             "/sudo - админ панель (требуются права)")



@dp.message(Command("me"))
async def infor(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)  # Добавляем пользователя в БД, если его нет
    user_data = get_user_data(user_id)  # Получаем данные пользователя
    
    if user_data:
        response = "\n".join([f"📌 {key}: {value}" for key, value in user_data.items()])
    else:
        response = "❌ Ошибка: данные не найдены."

    await message.answer(f"✅ Личный кабинет:\n\n{response}")



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



@dp.message(Command("me"))
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



""" @dp.callback_query(lambda c: c.data == 'subscribe')
async def handle_subscribe(callback: types.CallbackQuery):
    await callback.answer('Введите ключи')
    await callback.message.answer(
        'Пожалуйста, перешлите сообщение от пользователя, чтобы получить его ID.'
    )

# Забираем user id из пересланного сообщения
@dp.message()
async def process_message(message: types.Message):
    if message.forward_from:
        user_id = message.forward_from.id
        if get_user_data(user_id):  # Используем реальное имя вашей функции
            await message.answer(f"Получен пересланный ID пользователя: {user_id}. Пользователь есть в базе данных.")
            await message.answer("Выберите период подписки для пользователя: ", reply_markup=menu.defShowBotAdminSelectSub())
        else:
            await message.answer(f"Получен пересланный ID пользователя: {user_id}. Пользователя нет в базе данных.")
    elif message.reply_to_message and "Пожалуйста, перешлите сообщение" in message.reply_to_message.text:
        await message.answer("Пожалуйста, перешлите сообщение от пользователя, а не отправляйте обычный текст.")

 """

@dp.callback_query(lambda c: c.data == 'subscribe')
async def handle_subscribe(callback: types.CallbackQuery):
    await callback.answer('Введите ключи')
    await callback.message.answer(
        'Пожалуйста, перешлите сообщение от пользователя, чтобы получить его ID.'
    )

@dp.message()
async def process_message(message: types.Message, state: FSMContext):
    if message.forward_from:
        user_id = message.forward_from.id
        if get_user_data(user_id):  # Используем реальное имя вашей функции
            await message.answer(f"Получен пересланный ID пользователя: {user_id}. Пользователь есть в базе данных.")
            await message.answer("Выберите период подписки для пользователя: ", reply_markup=menu.defShowBotAdminSelectSub())
            # Сохраняем ID пользователя в состоянии
            await state.set_state(SubscriptionStates.waiting_for_subscription)
            await state.update_data(user_id=user_id)
        else:
            await message.answer(f"Получен пересланный ID пользователя: {user_id}. Пользователя нет в базе данных.")
    elif message.reply_to_message and "Пожалуйста, перешлите сообщение" in message.reply_to_message.text:
        await message.answer("Пожалуйста, перешлите сообщение от пользователя, а не отправляйте обычный текст.")
        
# Установка подписки для пользователя

# Подписка на 3 дня
@dp.callback_query(lambda c: c.data == '3_days')
async def handle_3_days_subscription(callback: types.CallbackQuery, state: FSMContext):
    # Получаем сохраненный ID пользователя из состояния
    data = await state.get_data()
    user_id = data.get('user_id')
    
    if user_id:
        # Вызываем функцию для установки подписки
        result = setSubFor_3_days(user_id)
        
        # Отправляем мгновенное уведомление пользователю
        await callback.answer("Подписка обновлена", show_alert=True)
        
        # Отправляем подробный результат в чат
        await callback.message.answer(result)
        
        # Сбрасываем состояние
        await state.clear()
    else:
        await callback.answer("Ошибка: ID пользователя не найден", show_alert=True)
        await callback.message.answer("Пожалуйста, начните процесс заново.")

    # Удаляем клавиатуру после обработки
    await callback.message.edit_reply_markup(reply_markup=None)


# Подписка на 7 дней
@dp.callback_query(lambda c: c.data == '7_days')
async def handle_7_days_subscription(callback: types.CallbackQuery, state: FSMContext):
    # Получаем сохраненный ID пользователя из состояния
    data = await state.get_data()
    user_id = data.get('user_id')
    
    if user_id:
        # Вызываем функцию для установки подписки
        result = setSubFor_7_days(user_id)
        
        # Отправляем мгновенное уведомление пользователю
        await callback.answer("Подписка обновлена", show_alert=True)
        
        # Отправляем подробный результат в чат
        await callback.message.answer(result)
        
        # Сбрасываем состояние
        await state.clear()
    else:
        await callback.answer("Ошибка: ID пользователя не найден", show_alert=True)
        await callback.message.answer("Пожалуйста, начните процесс заново.")

    # Удаляем клавиатуру после обработки
    await callback.message.edit_reply_markup(reply_markup=None)

# Подписка на 30 дней
@dp.callback_query(lambda c: c.data == '30_days')
async def handle_30_days_subscription(callback: types.CallbackQuery, state: FSMContext):
    # Получаем сохраненный ID пользователя из состояния
    data = await state.get_data()
    user_id = data.get('user_id')
    
    if user_id:
        # Вызываем функцию для установки подписки
        result = setSubFor_30_days(user_id)
        
        # Отправляем мгновенное уведомление пользователю
        await callback.answer("Подписка обновлена", show_alert=True)
        
        # Отправляем подробный результат в чат
        await callback.message.answer(result)
        
        # Сбрасываем состояние
        await state.clear()
    else:
        await callback.answer("Ошибка: ID пользователя не найден", show_alert=True)
        await callback.message.answer("Пожалуйста, начните процесс заново.")

    # Удаляем клавиатуру после обработки
    await callback.message.edit_reply_markup(reply_markup=None)

# Подписка на 365 дней
@dp.callback_query(lambda c: c.data == '365_days')
async def handle_365_days_subscription(callback: types.CallbackQuery, state: FSMContext):
    # Получаем сохраненный ID пользователя из состояния
    data = await state.get_data()
    user_id = data.get('user_id')
    
    if user_id:
        # Вызываем функцию для установки подписки
        result = setSubFor_365_days(user_id)
        
        # Отправляем мгновенное уведомление пользователю
        await callback.answer("Подписка обновлена", show_alert=True)
        
        # Отправляем подробный результат в чат
        await callback.message.answer(result)
        
        # Сбрасываем состояние
        await state.clear()
    else:
        await callback.answer("Ошибка: ID пользователя не найден", show_alert=True)
        await callback.message.answer("Пожалуйста, начните процесс заново.")

    # Удаляем клавиатуру после обработки
    await callback.message.edit_reply_markup(reply_markup=None)



@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text if message.text else 'А где текст?')



# for admin











    
