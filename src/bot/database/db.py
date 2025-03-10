# db.py

import os
from dotenv import load_dotenv
import sqlite3
import time

# Загрузка переменных из .env файла
load_dotenv()
ADMIN_ID = os.environ.get('adminID')

# Глобальная переменная для хранения номера строки пользователя
u_line = None

# Подключение к базе данных
def connect_db():
    return sqlite3.connect("src\\data\\users.db")

# Функция создания таблицы (если не создана)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS "Users" ( 
            "id" INTEGER PRIMARY KEY AUTOINCREMENT, 
            "user_id" INTEGER UNIQUE NOT NULL, 
            "active" INTEGER DEFAULT 1, 
            "created_at" INTEGER NOT NULL, 
            "trial_plan" INTEGER DEFAULT 1, 
            "trusting" INTEGER DEFAULT 0, 
            "t1" INTEGER DEFAULT 0, 
            "t2" INTEGER DEFAULT 0, 
            "t3" INTEGER DEFAULT 0, 
            "t4" INTEGER DEFAULT 0, 
            "admin" INTEGER DEFAULT 0 
        ) 
    ''')
    
    conn.commit()
    conn.close()
create_table()

# Функция добавления пользователя
def add_user(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    
    # Проверяем, есть ли пользователь уже в БД
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if user is None:
        current_timestamp = int(time.time())
        is_admin = 1 if user_id == ADMIN_ID else 0
        cursor.execute(''' 
            INSERT INTO Users (user_id, created_at, admin) 
            VALUES (?, ?, ?) 
        ''', (user_id, current_timestamp, is_admin))
        conn.commit()
        u_line = None  # Сбрасываем глобальную переменную, так как данные пользователя обновлены
    else:
        u_line = user[0]  # Сохраняем номер строки в глобальную переменную
    
    conn.close()

# Функция обновления триал-плана для конкретного пользователя
def update_trial_plan_for_user(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    current_time = int(time.time())
    
    cursor.execute("SELECT created_at FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        registration_time = user[0]
        difference = current_time - registration_time
        
        if difference >= 3 * 24 * 3600:  # 3 days in seconds
            cursor.execute("UPDATE Users SET trial_plan = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            
            # Обновляем глобальную переменную, если она не None
            if u_line is not None:
                u_line = cursor.fetchone()[0] if cursor.fetchone() else None
                
    conn.close()

# Функция получения всех данных пользователя
def get_user_data(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT active, created_at, trial_plan, trusting, t1, t2, t3, t4, admin 
        FROM Users WHERE user_id = ? 
    """, (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        u_line = user[0]  # Сохраняем номер строки в глобальную переменную
        return {
            "Активность": "Активный" if user[0] == 1 else "Неактивный",
            "Дата регистрации": get_user_time_registration(user[1]),
            "Триал-план": "Да" if user[2] == 1 else "Нет",
            "Доверие": user[3],
            "T1": user[4],
            "T2": user[5],
            "T3": user[6],
            "T4": user[7],
            "Админ": "Да" if user[8] == 1 else "Нет",
        }
    return None

# Функция получения времени регистрации пользователя
def get_user_time_registration(created_at):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_at))

# Функция для вычисления времени до окончания триал-подписки
def calculate_remaining_time(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT created_at FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        registration_time = user[0]
        current_time = int(time.time())
        difference = current_time - registration_time
        
        if difference >= 3 * 24 * 3600:  # 3 days in seconds
            remaining_time = 0
        else:
            remaining_time = 3 * 24 * 3600 - difference
        
        conn.close()
        
        days = remaining_time // (24 * 3600)
        hours = (remaining_time % (24 * 3600)) // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        
        return f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
    
    conn.close()
    return "Ошибка при вычислении времени"


# Функция для получения номера строки пользователя в базе данных
def get_user_row_number(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        u_line = user[0]  # Сохраняем номер строки в глобальную переменную
    else:
        u_line = None
    
    conn.close()
    return u_line


# Функция для проверки активности подписки и возврата разницы в разрядах
def is_trial_plan_active(user_id):
    global u_line
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT created_at FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        registration_time = user[0]
        current_time = int(time.time())
        difference = current_time - registration_time
        
        print(f"Текущее время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
        print(f"Регистрационное время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(registration_time))}")
        print(f"Разность времени: {difference} секунд")
        
        days = difference // (24 * 3600)
        hours = (difference % (24 * 3600)) // 3600
        minutes = (difference % 3600) // 60
        seconds = difference % 60
        
        print(f"Разность в днях: {days} дней")
        print(f"Разность в часах: {hours} часов")
        print(f"Разность в минутах: {minutes} минут")
        print(f"Разность в секундах: {seconds} секунд")
        
        if 0 < difference < 3 * 24 * 3600:  # Between 0 and 3 days in seconds
            return {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            }
        else:
            return None
    
    conn.close()
    return None