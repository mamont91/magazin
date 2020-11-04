import asyncio
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType)
from aiogram.utils.callback_data import CallbackData
import keyboard as kb
import database
import states
from config import lp_token, stikcer_OK, stikcer_gerl, stiker_kit
from load_all import dp, bot, _

db = database.DBCommands()

# Используем CallbackData для работы с коллбеками, в данном случае для работы с покупкой товаров
buy_item = CallbackData("buy", "item_id")


# Показываем список доступных товаров
@dp.message_handler(commands=["items"])
async def show_items(message: Message):
    # Достаем товары из базы данных
    all_items = await db.show_items()
    # Проходимся по товарам, пронумеровывая
    for num, item in enumerate(all_items):
        text = _("<b>Товар</b> \t№{id}: <u>{name}</u>\n"
                 "<b>Цена:</b> \t{price:,} грн\n")
        markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    # Создаем кнопку "купить" и передаем ее айдишник в функцию создания коллбека
                    InlineKeyboardButton(text=_("Купить 💵"), callback_data=buy_item.new(item_id=item.id))
                ]
                #         [InlineKeyboardButton(text=_("Наложеный платёж"), callback_data="NALOG")],
                # [InlineKeyboardButton(text=_("Отмена"), callback_data="close")]
            ]
        )

        # Отправляем фотку товара с подписью и кнопкой "купить"
        await message.answer(text=text.format(
            id=item.id,
            name=item.name,
            price=item.price / 100
        ),
            reply_markup=markup)
        # await message.answer_photo(
        #     photo=item.photo,
        #     caption=text.format(
        #         id=item.id,
        #         name=item.name,
        #         price=item.price / 100
        #     ),
        #     reply_markup=markup
        # )
        # Между сообщениями делаем небольшую задержку, чтобы не упереться в лимиты
        await asyncio.sleep(0.3)
    await message.answer(_("Доступные команды 🔍 : /help\n"
                           "Наши контакты ☎ : /contact\n"
                           "Условия доставки 🚚  : /delivery"),reply_markup=kb.markup_back)


# Для фильтрования по коллбекам можно использовать buy_item.filter()
@dp.callback_query_handler(buy_item.filter())
async def buying_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    # То, что мы указали в CallbackData попадает в хендлер под callback_data, как словарь, поэтому достаем айдишник
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()
    # markup = InlineKeyboardMarkup(
    #     inline_keyboard=
    #     [
    #         [InlineKeyboardButton(text=_("Отмена"), callback_data="close")],
    #         [InlineKeyboardButton(text=_("Наложеный платёж"), callback_data="NALOG")],
    #     ]
    # )
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            # [InlineKeyboardButton(text=_("Наложеный платёж"), callback_data="NALOG")],
            [InlineKeyboardButton(text=_("Отмена ❌ "), callback_data="close")]
        ]
    )

    # Достаем информацию о товаре из базы данных
    item = await database.Item.get(item_id)
    if not item:
        await call.message.answer(_("Такого товара не существует"))
        return

    text = _("Вы хотите купить товар \"<b>{name}</b>\" 👍\n"
             "Цена: <i>{price:,} грн/шт.</i>\n\n"
             "Возможна оплтата с помощью LiqPay.💳💰\n"
             "Или мы можем отправить Вам товар наложеным платежем.🚚\n\n"
             "Если хотите продолжить введите количество <b>{name}</b>").format(name=item.name,
                                                             price=item.price / 100)
    await call.message.answer_photo(photo=item.photo)
    await call.message.answer(text, reply_markup=markup)
    await states.Purchase.EnterQuantity.set()

    # Сохраняем в ФСМ класс товара и покупки
    await state.update_data(
        item=item,
        purchase=database.Purchase(
            item_id=item_id,
            purchase_time=datetime.datetime.now(),
            buyer=call.from_user.id
        )
    )


# Принимаем в этот хендлер только цифры
@dp.message_handler(regexp=r"^(\d+)$", state=states.Purchase.EnterQuantity)
async def enter_quantity(message: Message, state: FSMContext):
    # Получаем количество указанного товара
    quantity = int(message.text)
    if quantity == 0:
        await message.answer(_("Неверное значение."))
        await states.Purchase.EnterQuantity.set()
    else:
        async with state.proxy() as data:  # Работаем с данными из ФСМ
            data["purchase"].quantity = quantity
            item = data["item"]
            amount = item.price * quantity
            data["purchase"].amount = amount

    # Создаем кнопки
        agree_button = InlineKeyboardButton(
        text=_("Согласен"),
        callback_data="agree"
        )
        change_button = InlineKeyboardButton(
        text=_("Ввести количество заново"),
        callback_data="change"
        )
        cancel_button = InlineKeyboardButton(
        text=_("Отменить покупку"),
        callback_data="cancel"
        )

    # Создаем клавиатуру
        markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
            [agree_button],  # Первый ряд кнопок
            [change_button],  # Второй ряд кнопок
            [cancel_button]  # Третий ряд кнопок
            ]
        )
        await message.answer(
        _("Хорошо, вы хотите купить _ <i>{quantity}</i> _ \"<b>{name}</b>\" по цене <b>{price:,} грн/шт.</b>\n\n"
          "Получится <b>{amount:,}</b> грн. Подтверждаете?").format(
            quantity=quantity,
            name=item.name,
            amount=amount / 100,
            price=item.price / 100
            ),
        reply_markup=markup)
        await states.Purchase.Approval.set()


# То, что не является числом - не попало в предыдущий хендлер и попадает в этот
@dp.message_handler(state=states.Purchase.EnterQuantity)
async def not_quantity(message: Message):
    await message.answer(_("Неверное значение, введите число"))


# Если человек нажал на кнопку Отменить во время покупки - убираем все
@dp.callback_query_handler(text_contains="cancel", state=states.Purchase)
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки
    await call.message.answer(_("Вы отменили эту покупку"))
    ##################################################
    await bot.send_sticker(call.from_user.id, stiker_kit)
    await asyncio.sleep(0.5)
    await call.message.answer(_("Просмотреть товары: /items\n"
                                "Наши контакты: /contact"),reply_markup=kb.markup_back)
    await state.reset_state()


# Если человек нажал "ввести заново"
@dp.callback_query_handler(text_contains="change", state=states.Purchase.Approval)
async def approval(call: CallbackQuery):
    await call.message.edit_reply_markup()  # Убираем кнопки
    await call.message.answer(_("Введите количество товара заново."))
    await states.Purchase.EnterQuantity.set()


# Если человек нажал "согласен"
@dp.callback_query_handler(text_contains="agree", state=states.Purchase.Approval)
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки

    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    item: database.Item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()
    await purchase.create()
    await asyncio.sleep(0.5)
    await bot.send_message(chat_id=call.from_user.id,
                           text=_("Оплатите <b>{amount:,} грн.</b> используя LiqPay\n"
                                  "или оформив наложеный платеж ").format(amount=purchase.amount / 100))
    ################
    # --Ниже выбрать нужные параметры--
    # Пример заполнения можно посмотреть тут https://surik00.gitbooks.io/aiogram-lessons/content/chapter4.html
    # Но прошу обратить внимание, те уроки по старой версии aiogram и давно не обновлялись, так что могут быть
    # несостыковки.
    ################
    currency = "UAH"
    need_name = True
    need_phone_number = True
    need_email = False
    need_shipping_address = False
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Наложеный платёж 💸"), callback_data="NALOG")],
            [InlineKeyboardButton(text=_("Отмена ❌"), callback_data="close")]
        ]
    )

    await bot.send_invoice(chat_id=call.from_user.id,
                           title=item.name,
                           description=item.name,
                           payload=str(purchase.id),
                           start_parameter=str(purchase.id),
                           currency=currency,
                           prices=[
                               LabeledPrice(label=item.name, amount=purchase.amount)
                           ],
                           provider_token=lp_token,
                           need_name=need_name,
                           need_phone_number=need_phone_number,
                           need_email=need_email,
                           need_shipping_address=need_shipping_address
                           )
    await bot.send_message(chat_id=call.from_user.id, text=(_("⬇Оплата наложеным платежем⬇")), reply_markup=markup)
    await state.update_data(purchase=purchase)
    await states.Purchase.Payment.set()


@dp.pre_checkout_query_handler(state=states.Purchase.Payment)
async def checkout(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, True)
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    success = await check_payment(purchase)
    chat_id = query.from_user.id

    if success:
        await purchase.update(
            successful=True,
            shipping_address=query.order_info.shipping_address.to_python()
            if query.order_info.shipping_address
            else None,
            phone_number=query.order_info.phone_number,
            receiver=query.order_info.name,
            email=query.order_info.email
        ).apply()
        # await state.reset_state()
        markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [InlineKeyboardButton(text=_("Доставка"), callback_data="post")],
                [InlineKeyboardButton(text=_("Контакты"), callback_data="contacts")],
                [InlineKeyboardButton(text=_("Отмена ❌"), callback_data="close")]
            ]
        )

        await bot.send_message(chat_id, _("Спасибо за покупку,"))
        await bot.send_sticker(chat_id, sticker=stikcer_OK)
        await asyncio.sleep(1.0)
        await bot.send_message(chat_id, _("Мы можем организовать доставку\n"
                                          "или можете забрать\nв нашем магазине ☎ : /contact\n"
                                          "Просмотреть товары: 📦 /items\n"
                                          ),reply_markup=markup)

    else:
        await bot.send_message(chat_id, _("Покупка не была подтверждена, попробуйте позже..."))


async def check_payment(purchase: database.Purchase):
    return True


@dp.callback_query_handler(text_contains="NALOG", state="*")
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    item: database.Item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()
    await asyncio.sleep(1.0)
    await bot.send_message(chat_id=call.from_user.id,
                           text=_("Вы заказали {name}.\nОбщая сумма <b>{amount:,} грн.</b>  "
                                  "").format(amount=purchase.amount / 100, name=item.name))
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Отмена ❌"), callback_data="close")]
        ]
    )
    await asyncio.sleep(1.5)
    await call.message.answer(_("Условия доставки:\n"
                                "1. Доставка без предоплаты\n"
                                "2. При заказе от 2000 грн доставка по Киеву "
                                "и Киевской области бесплатно\n"
                                "3. Отправление товара в течении 2️⃣4️⃣ часов\n"
                                "4. В стоимость товара не включена стоимость доставки ❗\n"
                                "5. Товар обмену и возврату не подлежит ❗\n\n"
                                "Если хотите продолжить введите небходимую информацию"), reply_markup=markup)
    await asyncio.sleep(1.5)
    await call.message.answer(_("Напишите Ваши ФИО"))
    await states.Test.Q1.set()


@dp.message_handler(state=states.Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)
    await message.answer(_("Укажите пожалуйста Ваш номер телефона"))
    await states.Test.next()


@dp.message_handler(state=states.Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer(_("Укажите адрес доставки. Например Киев, отделение Новой Почты №99"))
    await states.Test.next()


@dp.message_handler(state=states.Test.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    # Достаем переменные
    user_name = message.from_user.full_name
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = message.text
    # answer4 = data.get("answer4")
    # answer5 = message.text
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    item: database.Item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()

    await message.answer(text=_("{answer1}, вы заказали <b>{name}</b>.\nОбщая сумма <b>{amount:,} грн.</b>\nОптлата налолежным "
                                "платежем\n"
                                "Ваш контактный телефон: {answer2}\n"
                                "Адрес доставки: {answer3}").format(amount=purchase.amount / 100, name=item.name,
                                                                    answer3=answer3, answer1=answer1, answer2=answer2))
    await asyncio.sleep(1.5)
    await bot.send_message(-1001417763749, f"Звертається:  {user_name}.\nПІБ: {answer1}.\nТелефон: {answer2}.\n"
                                           f"Хоче придбати: {item.name}.\nналоженим платежем\n"
                                           f"На сумму: {purchase.amount / 100} грн\n"
                                           f"Адреса доставки: {answer3}.")
    await asyncio.sleep(1.4)
    await message.answer(_("Ваша заявка принята в работу, отправка товара в течении 24 часов!"))
    await bot.send_sticker(message.chat.id, stikcer_gerl)
    await asyncio.sleep(1.4)
    await bot.send_message(message.chat.id, _("Просмотреть товары 📦 : /items\n"
                                              "Наши контакты ☎ : /contact"),reply_markup=kb.markup_back)

    # Вариант 1
    await state.finish()


# Если человек нажал на кнопку Отменить во время покупки - убираем все
@dp.callback_query_handler(text_contains="close", state="*")
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()  # Убираем кнопки
    await bot.send_sticker(call.from_user.id, stiker_kit)
    await call.message.answer(_("Вы отменили эту покупку"))
    await asyncio.sleep(0.5)
    await call.message.answer(_("Просмотреть товары 📦 : /items\n"
                                "Доступные команды 🔍 : /help\n"
                                "Наши контакты ☎️: /contact\n"
                                "Условия доставки 🚚 :/delivery"),reply_markup=kb.markup_back)
    await state.reset_state()



@dp.callback_query_handler(text_contains="post", state="*")
async def approval(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    item: database.Item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()
    await asyncio.sleep(1.0)
    await bot.send_message(chat_id=call.from_user.id,
                           text=_("Вы преобрели {name}. Общая сумма <b>{amount:,} грн.</b>  "
                                  "").format(amount=purchase.amount / 100, name=item.name))
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Отмена ❌"), callback_data="close")]
        ]
    )
    await asyncio.sleep(1.5)
    await call.message.answer(_("Условия доставки:\n"
                                "1. Доставка без предоплаты\n"
                                "2. При заказе от 2000 грн доставка по Киеву "
                                "и Киевской области бесплатно\n"
                                "3. Отправление товара в течении 2️⃣4️⃣ часов\n"
                                "4. В стоимость товара не включена стоимость доставки ❗\n"
                                "5. Товар обмену и возврату не подлежит ❗\n\n"
                                "Если хотите продолжить введите небходимую информацию"), reply_markup=markup)
    await asyncio.sleep(1.5)
    await call.message.answer(_("Напишите Ваши ФИО"))
    await states.Purchase.Name_delivery.set()


@dp.message_handler(state=states.Purchase.Name_delivery)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(answer1=answer)
    await message.answer(_("Укажите пожалуйста Ваш номер телефона"))
    await states.Purchase.Phone_delivery.set()


@dp.message_handler(state=states.Purchase.Phone_delivery)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer(_("Укажите адрес доставки. Например Киев, отделение Новой Почты №99"))
    await states.Purchase.Adress_delivery.set()


@dp.message_handler(state=states.Purchase.Adress_delivery)
async def answer_q3(message: types.Message, state: FSMContext):
    # Достаем переменные
    user_name = message.from_user.full_name
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = message.text
    # answer4 = data.get("answer4")
    # answer5 = message.text
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    item: database.Item = data.get("item")
    # Теперь можно внести данные о покупке в базу данных через .create()

    await message.answer(text=_("Вы купили <b>{name}</b>.\nОбщая сумма <b>{amount:,} грн.</b>\n"
                                "Оптлата с помощью LiqPay\n"
                                "Адрес доставки: {answer3}\n").format(amount=purchase.amount / 100, name=item.name,
                                                                    answer3=answer3))
    await asyncio.sleep(1.5)
    await bot.send_message(-1001417763749, f"Звертається:  {user_name}. \nПІБ: {answer1}.\nТелефон: {answer2}."
                                           f" Придбав: {item.name}.\nНа сумму: {purchase.amount / 100} грн\n"
                                           f"Адреса доставки: {answer3}.")
    await asyncio.sleep(1.4)
    await message.answer(_("Ваша заявка принята в работу, отправка товара в течении 24 часов!"))
    await bot.send_sticker(message.chat.id, stikcer_gerl)
    await asyncio.sleep(1.4)
    await bot.send_message(message.chat.id, _("Просмотреть товары 📦 : /items\n"
                                              "Наши контакты ☎️:  /contact"),reply_markup=kb.markup_back)

    # Вариант 1
    await state.finish()


@dp.message_handler(content_types=ContentType.STICKER)
async def other_echo(message: Message):
    print(message)


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def other_echo(message: Message):
    print(message)

@dp.message_handler(content_types=ContentType.PHOTO)
async def other_echo(message: Message):
    print(message)