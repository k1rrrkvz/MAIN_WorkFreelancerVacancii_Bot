from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

""" def user():

    user_cmdKB = InlineKeyboardMarkup(resize_keyboard=3)
    buttonVacancies = InlineKeyboardButton(text="/vacancies")
    buttonTarifs = InlineKeyboardButton(text="/tarifs")
    buttonProfile = InlineKeyboardButton(text="/profile")

    user_cmdKB.add(buttonVacancies)
    user_cmdKB.add(buttonTarifs)
    user_cmdKB.add(buttonProfile)

    return user_cmdKB """


def admin():
    admin_cmdKB = InlineKeyboardMarkup()  # Убираем resize_keyboard
    buttonVacancies = InlineKeyboardButton(text="Vacancies", callback_data="vacancies")
    buttonTarifs = InlineKeyboardButton(text="Tarifs", callback_data="tarifs")
    buttonProfile = InlineKeyboardButton(text="Profile", callback_data="profile")
    buttonAdminPanel = InlineKeyboardButton(text="sudo", callback_data="sudo")

    admin_cmdKB.add(buttonVacancies, buttonTarifs, buttonProfile, buttonAdminPanel)

    return admin_cmdKB