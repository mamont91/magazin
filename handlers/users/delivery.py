import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

import database
import states
from config import stikcer_OK
from load_all import dp, bot, _

db = database.DBCommands()


@dp.message_handler(commands=['delivery'], state=None)
async def enter_test(message: types.Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Назад ⬅️"), callback_data="back")]
        ]
    )
    await message.answer(_("Условия доставки:\n"
                                "1. Доставка без предоплаты\n"
                                "2. При заказе от 2000 грн доставка по Киеву "
                                "и Киевской области бесплатно\n"
                                "3. Отправление товара в течении 2️⃣4️⃣ часов\n"
                                "4. В стоимость товара не включена стоимость доставки ❗\n"
                                "5. Товар обмену и возврату не подлежит ❗"), reply_markup=markup)


@dp.callback_query_handler(text_contains="back", state="*")
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки

    main_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=_("Товары"), callback_data="ITEMS")],
            [
                # InlineKeyboardButton(text="Пользовательское соглашение", callback_data="Delivery"),
                InlineKeyboardButton(text=_("Контакты"), callback_data="contacts"),
            ]
        ]
    )
    await asyncio.sleep(0.5)
    await call.message.answer(_("Используйте доступные команды: /help\n\n"
                                "или пользуйтесь клавиатурой"), reply_markup=main_markup)
    await state.reset_state()




    #
    # await message.answer(_("Напишите ФИО получателя"))
#     await states.Test1.Q1.set()
#
#
# @dp.message_handler(state=states.Test1.Q1)
# async def answer_qt1(message: types.Message, state: FSMContext):
#     answer = message.text
#     # Вариант 1 сохранения переменных - записываем через key=var
#     await state.update_data(answer1=answer)
#     await message.answer(_("Укажите пожалуйста номер телефона получателя"))
#     await states.Test1.next()
#
#
# @dp.message_handler(state=states.Test1.Q2)
# async def answer_qt2(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(answer2=answer)
#     await message.answer(_("Укажите пожалуйста название товара"))
#     await states.Test1.next()
#
#
# @dp.message_handler(state=states.Test1.Q3)
# async def answer_qt3(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(answer3=answer)
#     await message.answer(_("Укажите пожалуйста количество товара"))
#     await states.Test1.next()
#
#
# @dp.message_handler(state=states.Test1.Q4)
# async def answer_qt4(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(answer4=answer)
#     await message.answer(_("Укажите адрес доставки. Например Киев, отделение Новой Почты №99"))
#     await states.Test1.next()
#
#
# @dp.message_handler(state=states.Test1.Q5)
# async def answer_qt5(message: types.Message, state: FSMContext):
#     # Достаем переменные
#     user_name = message.from_user.full_name
#     data = await state.get_data()
#     answer1 = data.get("answer1")
#     answer2 = data.get("answer2")
#     answer3 = data.get("answer3")
#     answer4 = data.get("answer4")
#     answer5 = message.text
#
#     await bot.send_message(-1001417763749, f"Звертається:  {user_name}. \n ПІБ: {answer1}. Телефон: {answer2}."
#                                            f" Товар: {answer3}  кількість: {answer4} "
#                                            f"Організувати доставку: {answer5}.")
#
#     await bot.send_sticker(message.chat.id, stikcer_OK)
#     await message.answer(_("Ваша заявка принята в работу, отправка товара в течении 24 часов!"))
#     await asyncio.sleep(1.4)
#     await bot.send_message(message.chat.id, _("Просмотреть товары: /items\n"
#                                               "Наши контакты: /contact"))
#
#     # Вариант 1
#     await state.finish()
