import os
from dotenv import load_dotenv

load_dotenv()

# Токен от BotFather
TOKEN_TG = os.getenv("TOKEN_TG")
# Токен от OpenWeatherMap
TOKEN_OWM = os.getenv("TOKEN_OWM")
# Урла API Telegram, до этого было зеркало
TG_API_URL = "https://api.telegram.org/bot"