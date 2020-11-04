import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
lp_token = os.getenv("LIQPAY_TOKEN")
host = "localhost"

I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

sticker2_start = "AAMCAgADGQEAAg0JX4LbcU0bUOWgDN0xkENFI1O2iPsAAqAJAAJ5XOIJnVf3RMcrpfOX9oUPAAQBAAdtAAN6hQACGwQ"
stikcer_OK2 = "CAACAgIAAxkBAAINB1-C2vRiiYj1jWIqzS6DlNjToXQtAAKgCQACeVziCZ1X90THK6XzGwQ"
stikcer_gerl = os.getenv("stiker_gerl")
stikcer_OK = os.getenv("stikcer_OK")
stiker_kit = os.getenv("stiker_kit")
sticker_start = os.getenv("sticker_start")
sticker_help = os.getenv("sticker_help")
sticker_neznau = os.getenv("sticker_neznau")
sticker_custom = os.getenv("sticker_custom")
#Файл
costum_id = os.getenv("costum_id")
visa = os.getenv("visa")
price = os.getenv("price")
AHD1000ml = os.getenv("AHD1000ml")
AHD60ml = os.getenv("AHD60ml")
AHD250ml = os.getenv("AHD250ml")
AHD_gel_75ml = os.getenv("AHD_gel_75ml")
AHD_gel_1000ml = os.getenv("AHD_gel_1000ml")
blanidas_active = os.getenv("blanidas_active")
blanidas_soft = os.getenv("blanidas_soft")


