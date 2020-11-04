from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from load_all import _

main_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
           # [InlineKeyboardButton(text=_("Товары"), callback_data="ITEMS")],
            [InlineKeyboardButton(text=_("Товары"), callback_data="items_all")],
            [
                InlineKeyboardButton(text=_("Условия доставки"), callback_data="Delivery"),
                InlineKeyboardButton(text=_("Контакты"), callback_data="contacts"),
            ],
            [
                InlineKeyboardButton(text=_("Способы оплаты"), callback_data="pay"),
                InlineKeyboardButton(text=_("Про компанию"), callback_data="company"),
            ],
            [InlineKeyboardButton(text=_("Пользовательское соглашение"), callback_data="usersugoda")]
        ]
    )

markup_back = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text=_("Главное меню 🔙"), callback_data="nazad")]
    ]
)

markup_buy = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text=_("Купить 💷"), callback_data="ITEMS")]
    ]
)

