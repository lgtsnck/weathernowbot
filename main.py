from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import pyowm
import config

CALLBACK_BUTTON_RUSSIAN_LANGUAGE = "callback_button_russian_language"
CALLBACK_BUTTON_ENGLISH_LANGUAGE = "callback_button_english_language"

TITLES = {
    CALLBACK_BUTTON_RUSSIAN_LANGUAGE: "Русский 🇷🇺",
    CALLBACK_BUTTON_ENGLISH_LANGUAGE: "English 🇬🇧/🇺🇸",
}


def get_language_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_RUSSIAN_LANGUAGE],
                                 callback_data=CALLBACK_BUTTON_RUSSIAN_LANGUAGE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ENGLISH_LANGUAGE],
                                 callback_data=CALLBACK_BUTTON_ENGLISH_LANGUAGE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Я бот погоды, список доступных команд есть в меню 👇🏻\n"
             "Я умею показывать погоду на данный момент 😉\n"
             "И еще, старайся вводить название своего города латинницей, я плохо понимаю по-русски 😅\n"
             "Чуть не забыл, выбери язык выдаваемой погоды 👇🏻",
        reply_markup=get_language_keyboard(),
    )


def help_message(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Надо же! Ты обратился ко мне за помощью 🙄\n"
             "Так уж и быть я тебе помогу 😚\n"
             "Напомню тебе, что я бот погоды. Ты можешь узнать погоду на данный момент командой /show_weather + название или индекс твоего города.\n"
             "И помни, что список доступных команд есть в меню 👇🏻\n",
    )


def change_language(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Выбери язык/Choose language",
        reply_markup=get_language_keyboard(),
    )


def keyboard_callback_handler(bot: Bot, update: Update):
    global select_language
    query = update.callback_query
    selector = query.data

    if selector == CALLBACK_BUTTON_RUSSIAN_LANGUAGE:
        select_language = "ru"
        bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Язык успешно выбран 🇷🇺",
        )
    elif selector == CALLBACK_BUTTON_ENGLISH_LANGUAGE:
        select_language = "en"
        bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Language successfully selected 🇬🇧/🇺🇸"
        )
    return select_language


def show_weather(bot: Bot, update: Update, args):
    city = ''.join(str(x) for x in args)
    owm = pyowm.OWM(config.TOKEN_OWM, language=select_language)
    city_weather = owm.weather_at_place(city)
    get_weather = city_weather.get_weather()
    wind = get_weather.get_wind()["speed"]
    deg_wind = get_weather.get_wind()["deg"]
    humidity = get_weather.get_humidity()
    description = get_weather.get_detailed_status()
    if select_language == "ru":
        temperature = get_weather.get_temperature("celsius")["temp"]
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"В городе {str(city)} сейчас {str(description)}\n"
                 f"Температура: {str(temperature)} °C\n"
                 f"Скорость ветра: {str(wind)} м/с\n"
                 f"Направление: {str(deg_wind)}°\n"
                 f"Влажность: {str(humidity)} %",
        )
    elif select_language == "en":
        temperature = get_weather.get_temperature("fahrenheit")["temp"]
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"In {str(city)} is {str(description)}\n"
                 f"Temperature: {str(temperature)} °F\n"
                 f"Wind: {str(wind)} meters per second\n"
                 f"Direction: {str(deg_wind)}°\n"
                 f"Humidity: {str(humidity)} %",
        )


def unknown_command(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Я такой команды не знаю, и ничего сделать не могу, у меня лапки 🌝\n"
             "Список доступных команд есть в меню 👇🏻"
    )


def main():
    bot = Bot(
        token=config.TOKEN_TG,
        base_url=config.TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", help_message)
    change_language_handler = CommandHandler("change_language", change_language)
    show_weather_handler = CommandHandler("show_weather", show_weather, pass_args=True)
    unknown_command_handler = MessageHandler(Filters.command, unknown_command)
    keyboard_callback = CallbackQueryHandler(callback=keyboard_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(change_language_handler)
    updater.dispatcher.add_handler(show_weather_handler)
    updater.dispatcher.add_handler(unknown_command_handler)
    updater.dispatcher.add_handler(keyboard_callback)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
