from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pyowm

import config

tg_token = config.TOKEN_TG
weather_token = config.TOKEN_OWM


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Привет! Я бот погоды, напиши мне свой город или  его индекс и я покажу тебе погоду на данный момент :) И еще, вводи название своего города латинницей, я пока что плохо понимаю по-русски',
    )


def show_weather(bot: Bot, update: Update):
    city = update.message.text
    owm = pyowm.OWM(weather_token, language='ru')
    city_weather = owm.weather_at_place(city)
    get_weather = city_weather.get_weather()
    temperature = get_weather.get_temperature()['temp']
    wind = get_weather.get_wind()['speed']
    humidity = get_weather.get_humidity()['humidity']
    description = get_weather.get_detailed_status()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'В городе{str(city)} сейчас {str(description)}\nТемпература: {str(temperature)} ℃\nСкорость ветра: {str(wind)} м/с\nВлажность: {str(humidity)} %',
    )


def main():
    bot = Bot(
        token=tg_token,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', do_start)
    show_weather_handler = MessageHandler(Filters.text, show_weather)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(show_weather_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
