import pyowm
from telegram import Update
from telegram.ext import CallbackContext

from database.get_user_settings import get_language
from locales import ru, en

import config


def show_weather(update: Update, context: CallbackContext):
    user_id = [update.message.chat_id]
    select_language = get_language(user_id)
    city = ''.join(str(x) for x in context.args)
    owm = pyowm.OWM(config.TOKEN_OWM)
    owm.config["language"] = select_language
    mgr = owm.weather_manager()
    city_weather = mgr.weather_at_place(city)
    get_weather = city_weather.weather
    wind = get_weather.wind()["speed"]
    deg_wind = get_weather.wind()["deg"]
    humidity = get_weather.humidity
    description = get_weather.detailed_status
    if select_language == "ru":
        temperature = get_weather.temperature("celsius")["temp"]
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=ru.FORECAST.format(city, description, temperature, wind, deg_wind, humidity),
        )
    elif select_language == "en":
        temperature = get_weather.temperature("fahrenheit")["temp"]
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=en.FORECAST.format(city, description, temperature, wind, deg_wind, humidity),
        )
