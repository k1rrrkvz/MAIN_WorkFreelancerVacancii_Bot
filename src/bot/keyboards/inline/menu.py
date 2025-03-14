from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def defShowBotUserMenu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Разместить вакансию", callback_data="vacancies"),
         InlineKeyboardButton(text="Помощь", callback_data="helps")],
        [InlineKeyboardButton(text="Тарифы", callback_data="tarifs"),
         InlineKeyboardButton(text="Профиль", callback_data="profile")]
    ]
                                )

def defShowBotAdminMenu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать id", callback_data="profile"),
         InlineKeyboardButton(text="Выдать подписку", callback_data="subscribe")]
    ]
                                )


def defShowBotAdminSelectSub():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="3 дня", callback_data="3_days"),
         InlineKeyboardButton(text="7 дней", callback_data="7_days"),
         InlineKeyboardButton(text="30 дней", callback_data="30_days"),
         InlineKeyboardButton(text="365 дней", callback_data="365_days")]
    ]
                                )