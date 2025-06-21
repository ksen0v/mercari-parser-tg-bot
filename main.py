from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
import asyncio

from utils.config_loader import BOT_TOKEN
from handlers.user_handlers import *
from utils.logger import logger


bot: Bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp: Dispatcher = Dispatcher()


async def main() -> None:
    dp.message.register(start_command, CommandStart())
    dp.message.register(spy_start_command, Command('spy'))
    dp.message.register(spy_stop_command, Command('spy_stop'))
    dp.message.register(spy_stop_all_command, Command('spy_stop_all'))
    dp.message.register(spy_list_command, Command('spy_list'))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())