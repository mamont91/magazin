from aiogram.types import ContentType, Message
import keyboard as kb
from config import sticker_neznau
from load_all import dp, bot, _


@dp.message_handler(content_types=ContentType.TEXT)
async def other_echo(message: Message):
    await bot.send_sticker(message.chat.id, sticker_neznau)
    await message.answer(_("Извините я Вас не понимаю используйте "
                           "пожалуйста доступные команды /help"),reply_markup=kb.main_markup)
