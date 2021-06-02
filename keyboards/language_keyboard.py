from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CALLBACK_BUTTON_RUSSIAN_LANGUAGE = "callback_button_russian_language"
CALLBACK_BUTTON_ENGLISH_LANGUAGE = "callback_button_english_language"

TITLES = {
    # CALLBACK_BUTTON_SETTINGS: "🛠",
    CALLBACK_BUTTON_RUSSIAN_LANGUAGE: "Русский 🇷🇺",
    CALLBACK_BUTTON_ENGLISH_LANGUAGE: "English 🇬🇧",
}


def get_language_keyboard():
    lang_keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_RUSSIAN_LANGUAGE],
                                 callback_data=CALLBACK_BUTTON_RUSSIAN_LANGUAGE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ENGLISH_LANGUAGE],
                                 callback_data=CALLBACK_BUTTON_ENGLISH_LANGUAGE),
        ],
    ]
    return InlineKeyboardMarkup(lang_keyboard)