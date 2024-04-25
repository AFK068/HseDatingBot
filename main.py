import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from data_base.models import async_main

from routers.main_router import router as main_router
from aiogram.enums import ParseMode

TOKEN = "7152407194:AAF14ffPSVRlF68aZcXSj_ZXZKrpETNqSDM"
bot = Bot(token=TOKEN)

dp = Dispatcher(bot=bot)
dp.include_router(main_router)


async def main() -> None:
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())