from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import database
from config import admin_id, sticker_start

from load_all import dp, bot, _
import keyboard as kb

# Для команды /start есть специальный фильтр, который можно тут использовать

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    user_name = message.from_user.full_name
    chat_id = message.from_user.id
    referral = message.get_args()
    user = await db.add_new_user(referral=referral)
    id = user.id
    count_users = await db.count_users()
    await bot.send_sticker(chat_id, sticker_start)

    # Отдадим пользователю клавиатуру с выбором языков
    languages_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Україньска 🇺🇦", callback_data="lang_uk")],
            [
                InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
                InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
            ]
        ]
    )

    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={id}"

    # Для многоязычности, все тексты, передаваемые пользователю должны передаваться в функцию "_"
    # Вместо "текст" передаем _("текст")

    text = _("{user_name}, Вас приветствует магазин\n"
             f"<b><u>Антисептики и Дезинфектанты</u></b>\n"
             "Просмотреть товары 📦 : /items\n"
             "Доступные команды 🔍 : /help").format(user_name=user_name)

    if message.from_user.id == admin_id:
        text += _("\n"
                  "Добавить новый товар: /add_item\n"
                  "Количество людей в базе данных {count_users}").format(
            count_users=count_users,
            bot_link=bot_link
        )
    await bot.send_message(chat_id, text, reply_markup=languages_markup)


# Альтернативно можно использовать фильтр text_contains, он улавливает то, что указано в call.data
@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    # Достаем последние 2 символа (например ru)
    lang = call.data[-2:]
    await db.set_language(lang)


    # После того, как мы поменяли язык, в этой функции все еще указан старый, поэтому передаем locale=lang

    await call.message.answer(_("Ваш язык был изменен"))
    await bot.send_message(chat_id=call.message.chat.id, text=_("Используйте клавиатуру ⬇️", locale=lang),
                           reply_markup=kb.main_markup)

