from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class Language_engl(BoundFilter):
    async def chek_lang(self,message: types.Message):
        return message.from_user.language_code == "eng"