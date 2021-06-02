from telegram import Update
from telegram.ext import CallbackContext

from database.add_delete_user import add_user
from database.get_user_settings import get_language
from database.set_user_settings import change_user_language
from keyboards.language_keyboard import get_language_keyboard, CALLBACK_BUTTON_RUSSIAN_LANGUAGE, \
    CALLBACK_BUTTON_ENGLISH_LANGUAGE
from locales import ru, en


def do_start(update: Update, context: CallbackContext):
    users_id = update.message.chat_id
    user_id = [update.message.chat_id]

    add_user(user_id, users_id)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hi {}! Let's do the first setup 👇🏻".format(update.message.chat.first_name),
        reply_markup=get_language_keyboard(),
    )


def change_language(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выбери язык/Choose language",
        reply_markup=get_language_keyboard(),
    )


def help_message(update: Update, context):
    user_id = [update.message.chat_id]
    select_language = get_language(user_id)
    if select_language == "ru":
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=ru.HELP_MESSAGE,
        )
    elif select_language == "en":
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=en.HELP_MESSAGE,
        )


def language_keyboard_callback_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query
    selector = query.data

    if selector == CALLBACK_BUTTON_RUSSIAN_LANGUAGE:
        change_user_language("ru", user_id)
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Язык успешно выбран 🇷🇺",
        )

    elif selector == CALLBACK_BUTTON_ENGLISH_LANGUAGE:
        change_user_language("en", user_id)
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Language successfully selected 🇬🇧"
        )


def unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=ru.UNKNOWN_COMMAND
    )