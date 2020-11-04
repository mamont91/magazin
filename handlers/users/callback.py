import asyncio

from messages import MESSAGES

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup,
                           KeyboardButton, MediaGroup)
from aiogram.utils.callback_data import CallbackData
import keyboard as kb
import database
import states
from config import AHD60ml, stikcer_gerl, sticker_help, visa, sticker_custom, costum_id, AHD1000ml, AHD250ml, price, \
    AHD_gel_75ml, AHD_gel_1000ml,blanidas_active,blanidas_soft
from load_all import dp, bot, _

db = database.DBCommands()

# Используем CallbackData для работы с коллбеками, в данном случае для работы с покупкой товаров
buy_item = CallbackData("buy", "item_id")


# Если человек нажал на кнопку Отменить во время покупки - убираем все
@dp.callback_query_handler(text_contains="ITEMS")
async def approval(call: CallbackQuery):
    await call.message.edit_reply_markup()  # Убираем кнопки
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
                ],
                # [InlineKeyboardButton(text=_("Наложеный платёж"), callback_data="NALOG")]
            ]
        )

        # Отправляем фотку товара с подписью и кнопкой "купить"
        await call.message.answer(text=text.format(
            id=item.id,
            name=item.name,
            price=item.price / 100
        ),
            reply_markup=markup)

        await asyncio.sleep(0.3)

    await call.message.answer(_("Доступные команды 🔍 : /help\n"
                                "Наши контакты ☎️: /contact\n"
                                "Условия доставки 🚚 :/delivery"), reply_markup=kb.markup_back)


@dp.callback_query_handler(text_contains="Delivery", state=None)
async def coll_delivery(call: CallbackQuery):
    await call.message.edit_reply_markup()  # Убираем кнопки
    main_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Товары"), callback_data="ITEMS")],
            [
                InlineKeyboardButton(text=_("Команды"), callback_data="commands"),
                InlineKeyboardButton(text=_("Контакты"), callback_data="contacts"),
            ],
            [InlineKeyboardButton(text=_("Назад 🔙"), callback_data="nazad")]
        ]
    )

    await call.message.answer(_("Условия доставки:\n"
                                "1. Доставка без предоплаты\n"
                                "2. При заказе от 2000 грн доставка по Киеву "
                                "и Киевской области бесплатно\n"
                                "3. Отправление товара в течении 2️⃣4️⃣ часов\n"
                                "4. В стоимость товара не включена стоимость доставки ❗\n"
                                "5. Товар обмену и возврату не подлежит ❗"), reply_markup=main_markup)

    # await asyncio.sleep(1.0)
    # await call.message.answer(_("Просмотреть товары: /items\n"
    #                                           "Доступные команды: /help"))


@dp.callback_query_handler(text_contains="contacts", state=None)
async def contacts(call: CallbackQuery):
    await call.message.edit_reply_markup()  # Убираем кнопки
    msg = call.message.chat.id
    await bot.send_sticker(msg, sticker=stikcer_gerl)
    await bot.send_message(msg, _("Контакты магазина:\n"
                                  "ФОП Лопушняк Олег Семенович ЗКПОУ 2690915715\n"
                                  "Юридический адрес: г. Киев, ул. Симиренка 2-Б, кв.104\n"
                                  "\nТелефоны: 0964492838, 0994908521"
                                  "\nЭлектронная почта: oleglopushnyak@ukr.net\n"
                                  "Адрес для самовывоза: г. Киев\nпроспект Леся Курбаса 2/13\nАптека Лекафарм\n"
                                  "График работы: ежедневно с 8:00 до 21:00"))
    await asyncio.sleep(1.0)
    await bot.send_message(msg, _("Просмотреть товары 📦 : /items\n"
                                  "Доступные команды 🔍 : /help"), reply_markup=kb.markup_back)


@dp.callback_query_handler(text_contains="commands", state=None)
async def commands(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    await bot.send_sticker(msg, sticker=sticker_help)
    await bot.send_message(msg, _("/start - Начать работу\n"
                                  "/items - 📦 Товары\n"
                                  "/delivery - 🚚  Условия доставки\n"
                                  "/custom - 📖 Пользовательское соглашение\n"
                                  "/contact - ☎ Контакты\n"), reply_markup=kb.markup_back)


@dp.callback_query_handler(text_contains="pay", state=None)
async def pay(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    await bot.send_photo(msg, visa)
    await bot.send_message(msg, _("Способы оплаты:\n"
                                  "1.Оплата будет происходить через выставление инвойса\n"
                                  "на E-mail через LiqPay\n"
                                  "2.Оплата на карту: 5168872771179180\n"
                                  "3.Наложеным платежем\n"
                                  "/contact - ☎ Контакты\n"), reply_markup=kb.markup_back)


@dp.callback_query_handler(text_contains="nazad", state=None)
async def pay(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    await bot.send_message(msg, _("Выберите тему обращения ⬇"), reply_markup=kb.main_markup)


@dp.callback_query_handler(text_contains="usersugoda", state=None)
async def pay(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    await bot.send_sticker(msg, sticker=sticker_custom)
    await bot.send_document(msg, costum_id)
    await asyncio.sleep(1.0)
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text=_("Принять"), callback_data="accept")]
        ]
    )
    await bot.send_message(msg, _("Ознакомьтесь и примите\nпользовательское соглашение ⬇"), reply_markup=markup)


@dp.callback_query_handler(text_contains="items_all", state=None)
async def pay(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    user_name = call.from_user.full_name
    album = MediaGroup()
    album.attach_photo(AHD1000ml)
    album.attach_photo(AHD250ml)
    album.attach_photo(AHD60ml)

    album_ahd_gel = MediaGroup()
    album_ahd_gel.attach_photo(AHD_gel_75ml)
    album_ahd_gel.attach_photo(AHD_gel_1000ml)

    album_blanidas=MediaGroup()
#    album_blanidas.attach_photo(blanidas_soft)
    album_blanidas.attach_photo(blanidas_active)

    await bot.send_message(msg, _("{user_name}, у нас Вы можете приобрести "
                                  "более 100 видов антисептиков и дезинфектантов. "
                                  "Некоторые из них представлены ниже ⬇").format(user_name=user_name))
    await asyncio.sleep(2)
    # ТЕКСТЫ описания товаров из MESSAGES
    text = MESSAGES['text']
    text_gel = MESSAGES['text_gel']
    text_blanidas=MESSAGES['blanidas']
# AHD express
    await bot.send_media_group(msg, media=album)
    await asyncio.sleep(2)
    await bot.send_message(msg, text=text)
    await asyncio.sleep(2)
    # AHD gel
    await bot.send_media_group(msg, media=album_ahd_gel)
    await bot.send_message(msg, text=text_gel)
    await asyncio.sleep(2)
    # blanidas
    await bot.send_media_group(msg,media=album_blanidas)
    await bot.send_message(msg, text=text_blanidas, reply_markup=kb.markup_buy)
    await bot.send_document(msg, document=price)
    await bot.send_message(msg, _("По остальным продуктам 👆 уточняйте\n"
                                  "у нашего менеджера /contact - ☎ Контакты"), reply_markup=kb.markup_back)


@dp.callback_query_handler(text_contains="company", state=None)
async def pay(call: CallbackQuery):
    await call.message.edit_reply_markup()
    msg = call.message.chat.id
    await bot.send_message(msg, _("В нашому інтернет магазині реалізуєтья продукція компанії Лізоформ."
                                  " На світовому ринку компанія "
                                  "успішно працює вже понад 120 років. Сьогодні слово «Лізоформ» по праву вважається"
                                  " символом дезінфекції в країнах Європи, СНД, Північної і Південної Америки,"
                                  " на території Азії, Африки, Австралії. Основним принципом компанії є незмінна висока"
                                  " якість продукції як гарантія захисту і безпеки життя. Вірність цьому принципу"
                                  " дотримується протягом всього часу існування компанії і передається із покоління"
                                  " в покоління. В Україні компанія «Лізоформ Медікал» з'явилася на початку 90-х років,"
                                  " як самостійна фірма зі своїми власними ідеями, підходами до бізнесу і незмінною "
                                  "вірністю німецькій традиції. Вже впродовж  20 років компанія «Лізоформ Медікал» є"
                                  " лідером в Україні по досягненню найвищих стандартів гігієни в сферах медицини, "
                                  "комунального господарства, харчової та фармацевтичної промисловості тощо. Місія "
                                  "компанії «Лізоформ Медікал» - впровадження новітніх технологій дезінфекції та "
                                  "гігієни "
                                  " з метою створення  безпечних умов для персоналу і клієнтів закладу. Ми впроваджуємо"
                                  " комплексний підхід до поставлених завдань забезпечення санітарно-гігієнічних та "
                                  "протиепідемічних режимів з використанням сучасних технологічних розробок систем"
                                  "чистоти. В своїх розробках ми використовуємо останні світові технологічні "
                                  "досягнення, "
                                  "які дають можливість оптимізувати процес прибирання і дезінфекції як в зменшенні "
                                  "витрат "
                                  " часу, економії людських ресурсів, так і в отриманні високих показників якості. "
                                  "«Лізоформ Медікал» є першою в Україні компанією по забезпеченню комплексних"
                                  " технологій профілактики внутрішньолікарняних інфекцій в лікувально-профілактичних"
                                  " закладах. Система гігієни «Лізоформ Медікал» включає в собі сучасні антисептичні"
                                  " та дезінфекційні засоби провідного виробника біоцидів «Лізоформ Др. Ханс Роземанн "
                                  "ГмбХ», які зареєстровані і дозволені до використання Міністерством охорони здоров'я "
                                  "України, а також професійні дозуючі пристрої, сучасне обладнання для прибирання"
                                  "«Вермоп» з метою раціонального використання засобів і досягнення найвищих "
                                  "стандартів "
                                  "чистоти. Слід зазначити, що на сьогоднішній день компанія «Лізоформ Медікал» "
                                  "налагодила виробництво на території України дезінфекційних і антисептичних "
                                  "засобів. Тепер лікувальні заклади у своїй практиці можуть використовувати доступні "
                                  "високоякісні засоби вітчизняного виробництва, розроблені за європейською "
                                  "рецептурою."), reply_markup=kb.markup_back)
