from aiogram import executor, types

from config import admin_id
from database import create_db
from load_all import bot

async def commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Почати роботу"),
        types.BotCommand("help", "Доступні команди"),
        types.BotCommand("items", "Товари"),
        types.BotCommand("delivery", "Умови доставки"),
        types.BotCommand("add_item", "дОбавить товар"),
        types.BotCommand("custom", "Угода користувача"),
        types.BotCommand("contact", "Контакти")
    ])

async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await create_db()
    await commands(dp)
    await bot.send_message(admin_id, "Я запущен!")


if __name__ == '__main__':
    from handlers.users.admin_panel import dp
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)




# from aiogram import types
# from aiogram.utils.executor import start_webhook
#
# from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, admin_id
# from load_all import SSL_CERTIFICATE, ssl_context, bot
# async def commands(dp):
#     await dp.bot.set_my_commands([
#         types.BotCommand("start", "Почати роботу"),
#         types.BotCommand("help", "Доступні команди"),
#         types.BotCommand("items", "Товари"),
#         types.BotCommand("delivery", "Умови доставки"),
#         types.BotCommand("add_item", "дОбавить товар"),
#         types.BotCommand("custom", "Угода користувача"),
#         types.BotCommand("contact", "Контакти")
#     ])
#
#
# async def on_startup(dp):
#     await bot.set_webhook(
#         url=WEBHOOK_URL,
#         certificate=SSL_CERTIFICATE
#     )
#     from handlers import filters
#     await filters.Language_engl.chek_lang(dp)
#     import language_middleware
#     language_middleware.setup_middleware(dp)
#
#     # import middlewares
#     # filters.setup(dp)
#     # middlewares.setup(dp)
#     await bot.send_message(admin_id, "Я запущен!")
#     await commands(dp)
#
#
# if __name__ == '__main__':
#     from handlers import dp
#
#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         on_startup=on_startup,
#         skip_updates=True,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#         ssl_context=ssl_context
#     )
