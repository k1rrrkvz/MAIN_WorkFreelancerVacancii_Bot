import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import logging

# Загрузка переменных из .env файла
load_dotenv()

appToken = os.environ.get('appToken', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
bot = Bot(token=appToken)



