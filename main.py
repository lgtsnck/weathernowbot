from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
import config
from commands.bot_api_commands import *
from commands.bot_owm_commands import show_weather


def main():
    updater = Updater(config.TOKEN_TG)

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", help_message)
    change_language_handler = CommandHandler("change_language", change_language)
    show_weather_handler = CommandHandler("show_weather", show_weather)
    unknown_command_handler = MessageHandler(Filters.command, unknown_command)
    language_keyboard_callback = CallbackQueryHandler(callback=language_keyboard_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(change_language_handler)
    updater.dispatcher.add_handler(show_weather_handler)
    updater.dispatcher.add_handler(unknown_command_handler)
    updater.dispatcher.add_handler(language_keyboard_callback)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
