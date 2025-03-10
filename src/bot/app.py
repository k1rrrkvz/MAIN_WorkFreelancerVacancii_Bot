import os
import sys
import asyncio
import logging

import handlers

from loader import dp, bot

async def main():
    await dp.start_polling(bot, skip_updates=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s [%(name)s] - %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        print("!Running")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("!Stopped")