import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery)

import database
from config import costum_id, stikcer_gerl, sticker_help, sticker_custom
from load_all import dp, bot, _

import keyboard as kb
db = database.DBCommands()


# @dp.message_handler(commands=["referrals"])
# async def check_referrals(message: types.Message):
#     referrals = await db.check_referrals()
#     text = _("Ваши рефералы:\n{referrals}").format(referrals=referrals)
#     await message.answer(text)
#

@dp.message_handler(commands=['contact'], state="*")
async def contact(message: types.Message, state: FSMContext):
    msg = message.chat.id
    await bot.send_sticker(msg, sticker=stikcer_gerl)
    await bot.send_message(msg, _("Контакты магазина:\n"
                                  "ФОП Лопушняк Олег Семенович ЗКПОУ 2690915715\n"
                                  "Юридический адрес: г. Киев, ул. Симиренка 2-Б, кв.104\n"
                                  "\nТелефоны: 0964492838, 0994908521"
                                  "\nЭлектронная почта: oleglopushnyak@ukr.net\n"
                                  "Адрес для самовывоза: г. Киев\nпроспект Леся Курбаса 2/13\nАптека Лекафарм\n"
                                  "График работы: ежедневно с 8:00 до 21:00"))
    await asyncio.sleep(1.0)
    await bot.send_message(message.chat.id, _("Просмотреть товары 📦 : /items\n"
                                              "Доступные команды 🔍 : /help"))


@dp.message_handler(commands=['help'], state="*")
async def contact(message: types.Message):
    msg = message.chat.id
    await bot.send_sticker(msg, sticker=sticker_help)
    await bot.send_message(msg, _("/start - Начать работу\n"
                                  "/items - 📦 Товары\n"
                                  "/delivery - 🚚  Условия доставки\n"
                                  "/custom - 📖 Пользовательское соглашение\n"
                                  "/contact - ☎ Контакты\n"))


@dp.message_handler(commands=['custom'], state="*")
async def contact(message: types.Message, state: FSMContext):
    msg = message.chat.id
    await bot.send_sticker(msg, sticker=sticker_custom)
    await bot.send_document(msg, costum_id)
    await asyncio.sleep(1.0)
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Принять"), callback_data="accept")]
        ]
    )

    await bot.send_message(msg, text=_("Ознакомьтесь и примите пожалуйста\nпользовательское соглашение 👇"),
                           reply_markup=markup)


@dp.callback_query_handler(text_contains="accept")
async def approval(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(text=_("Спасибо, можете использовать 🔍  /help\n"
                                     "Или вернитесь в главное меню"),reply_markup=kb.markup_back)
