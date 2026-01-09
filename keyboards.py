from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def generate_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="Weather 🌥️")
    markup.add(btn)
    return markup