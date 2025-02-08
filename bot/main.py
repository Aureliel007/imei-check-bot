import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config
import handlers


logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')
    config = load_config()
    users_list = config.users_ids
    bot = Bot(
        token=config.token
    )
    dp = Dispatcher()
    dp.workflow_data.update({'users_list': users_list})
    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
